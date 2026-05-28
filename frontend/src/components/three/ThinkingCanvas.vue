<template>
  <div ref="container" class="absolute inset-0 overflow-hidden pointer-events-none">
    <canvas ref="canvas" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as THREE from 'three'

const props = defineProps({
  active: {
    type: Boolean,
    default: false
  }
})

const container = ref(null)
const canvas = ref(null)

let scene, camera, renderer, mesh, animationId
let time = 0

const initScene = () => {
  // Scene setup
  scene = new THREE.Scene()

  // Camera
  camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.z = 5

  // Renderer
  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true,
    alpha: true
  })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x0a0a0f, 0.8)

  // Create orbital particle system
  const particleCount = 500
  const positions = new Float32Array(particleCount * 3)
  const colors = new Float32Array(particleCount * 3)

  for (let i = 0; i < particleCount; i++) {
    const i3 = i * 3
    
    // Spherical distribution for orbital paths
    const radius = 2 + Math.random() * 3
    const theta = Math.random() * Math.PI * 2
    const phi = Math.random() * Math.PI

    positions[i3] = radius * Math.sin(phi) * Math.cos(theta)
    positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
    positions[i3 + 2] = radius * Math.cos(phi)

    // Gradient from center to edge
    const dist = radius / 5
    const r = 0.39 * (1 - dist) + 0.51 * dist
    const g = 0.4 * (1 - dist) + 0.55 * dist
    const b = 0.95
    colors[i3] = r
    colors[i3 + 1] = g
    colors[i3 + 2] = b
  }

  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  // Particle material
  const material = new THREE.ShaderMaterial({
    uniforms: {
      time: { value: 0 },
      intensity: { value: 1.0 }
    },
    vertexShader: `
      attribute vec3 color;
      varying vec3 vColor;
      varying float vDist;
      uniform float time;
      uniform float intensity;
      
      void main() {
        vColor = color;
        
        vec3 pos = position;
        
        // Orbital rotation based on position
        float angle = time * 0.5 + length(position) * 0.5;
        mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
        pos.xy = rot * pos.xy;
        
        // Gentle pulsation
        float pulse = 1.0 + sin(time * 2.0 + length(position) * 2.0) * 0.1;
        pos *= pulse;
        
        vDist = length(pos) / 5.0;
        
        vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
        float size = mix(3.0, 1.0, vDist) * intensity;
        gl_PointSize = size * (10.0 / -mvPosition.z);
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      varying float vDist;
      
      void main() {
        float dist = length(gl_PointCoord - vec2(0.5));
        if (dist > 0.5) discard;
        
        float alpha = (1.0 - smoothstep(0.2, 0.5, dist)) * (1.0 - vDist * 0.5);
        gl_FragColor = vec4(vColor, alpha * 0.9);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  })

  const particles = new THREE.Points(geometry, material)
  scene.add(particles)

  // Central glowing sphere
  const coreGeometry = new THREE.SphereGeometry(0.5, 32, 32)
  const coreMaterial = new THREE.ShaderMaterial({
    uniforms: {
      time: { value: 0 }
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      uniform float time;
      
      void main() {
        vNormal = normal;
        vPosition = position;
        
        // Subtle pulsing
        vec3 pos = position * (1.0 + sin(time * 3.0) * 0.05);
        
        vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      uniform float time;
      
      void main() {
        float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.0);
        vec3 coreColor = vec3(0.5, 0.5, 1.0);
        float pulse = 0.8 + sin(time * 4.0) * 0.2;
        vec3 glowColor = mix(coreColor, vec3(0.7, 0.7, 1.0), fresnel) * pulse;
        gl_FragColor = vec4(glowColor, 0.6 + fresnel * 0.4);
      }
    `,
    transparent: true,
    side: THREE.DoubleSide
  })

  mesh = new THREE.Mesh(coreGeometry, coreMaterial)
  scene.add(mesh)

  // Orbital rings
  for (let i = 0; i < 3; i++) {
    const ringGeometry = new THREE.TorusGeometry(1.5 + i * 0.8, 0.02, 16, 100)
    const ringMaterial = new THREE.MeshBasicMaterial({
      color: 0x6366f1,
      transparent: true,
      opacity: 0.3 - i * 0.08
    })
    const ring = new THREE.Mesh(ringGeometry, ringMaterial)
    ring.rotation.x = Math.PI / 2 + (i - 1) * 0.3
    ring.rotation.z = i * 0.5
    scene.add(ring)
  }
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  time += 0.016

  // Update uniforms
  scene.children.forEach(child => {
    if (child.material && child.material.uniforms) {
      if (child.material.uniforms.time) {
        child.material.uniforms.time.value = time
      }
    }
  })

  // Rotate entire scene slowly
  scene.rotation.y = time * 0.1
  scene.rotation.x = Math.sin(time * 0.2) * 0.1

  // Intensity based on active prop
  if (mesh && mesh.material.uniforms) {
    const targetIntensity = props.active ? 1.0 : 0.5
    mesh.material.uniforms.intensity = targetIntensity
  }

  renderer.render(scene, camera)
}

const handleResize = () => {
  if (camera && renderer) {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  }
}

watch(() => props.active, (isActive) => {
  if (scene) {
    scene.children.forEach(child => {
      if (child.material && child.material.uniforms && child.material.uniforms.intensity) {
        child.material.uniforms.intensity.value = isActive ? 1.0 : 0.3
      }
    })
  }
})

onMounted(() => {
  initScene()
  animate()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
  
  if (renderer) {
    renderer.dispose()
  }
})
</script>