<template>
  <div ref="container" class="absolute inset-0 overflow-hidden">
    <canvas ref="canvas" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const container = ref(null)
const canvas = ref(null)

let scene, camera, renderer, particles, animationId

const initScene = () => {
  // Scene
  scene = new THREE.Scene()
  scene.fog = new THREE.FogExp2(0x0a0a0f, 0.002)

  // Camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.z = 30

  // Renderer
  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true,
    alpha: true
  })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x0a0a0f, 1)

  // Create particles
  const particleCount = 2000
  const positions = new Float32Array(particleCount * 3)
  const colors = new Float32Array(particleCount * 3)
  const sizes = new Float32Array(particleCount)

  for (let i = 0; i < particleCount; i++) {
    const i3 = i * 3
    
    // Grid-like distribution
    const gridSize = 50
    const cellSize = gridSize / Math.cbrt(particleCount)
    const gridPos = Math.floor(Math.random() * gridSize / cellSize) * cellSize
    
    positions[i3] = (Math.random() - 0.5) * gridSize
    positions[i3 + 1] = (Math.random() - 0.5) * gridSize
    positions[i3 + 2] = (Math.random() - 0.5) * gridSize * 2

    // Cyber accent colors
    const colorMix = Math.random()
    if (colorMix < 0.3) {
      // Purple accent
      colors[i3] = 0.4
      colors[i3 + 1] = 0.4
      colors[i3 + 2] = 0.95
    } else if (colorMix < 0.5) {
      // Light purple
      colors[i3] = 0.5
      colors[i3 + 1] = 0.55
      colors[i3 + 2] = 0.98
    } else {
      // White
      const brightness = 0.3 + Math.random() * 0.4
      colors[i3] = brightness
      colors[i3 + 1] = brightness
      colors[i3 + 2] = brightness
    }

    sizes[i] = Math.random() * 2 + 0.5
  }

  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1))

  // Shader material for particles
  const material = new THREE.ShaderMaterial({
    uniforms: {
      time: { value: 0 },
      pixelRatio: { value: renderer.getPixelRatio() }
    },
    vertexShader: `
      attribute float size;
      attribute vec3 color;
      varying vec3 vColor;
      uniform float time;
      uniform float pixelRatio;
      
      void main() {
        vColor = color;
        vec3 pos = position;
        
        // Gentle floating animation
        pos.y += sin(time * 0.3 + position.x * 0.1) * 0.5;
        pos.x += sin(time * 0.2 + position.y * 0.1) * 0.3;
        pos.z += sin(time * 0.25 + position.z * 0.1) * 0.4;
        
        vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
        gl_PointSize = size * pixelRatio * (20.0 / -mvPosition.z);
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      
      void main() {
        float dist = length(gl_PointCoord - vec2(0.5));
        if (dist > 0.5) discard;
        
        float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
        gl_FragColor = vec4(vColor, alpha * 0.8);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  })

  particles = new THREE.Points(geometry, material)
  scene.add(particles)

  // Add connecting lines
  const lineGeometry = new THREE.BufferGeometry()
  const linePositions = []
  const lineCount = 300

  for (let i = 0; i < lineCount; i++) {
    const p1 = new THREE.Vector3(
      (Math.random() - 0.5) * 50,
      (Math.random() - 0.5) * 50,
      (Math.random() - 0.5) * 100
    )
    const p2 = p1.clone().add(new THREE.Vector3(
      (Math.random() - 0.5) * 10,
      (Math.random() - 0.5) * 10,
      (Math.random() - 0.5) * 10
    ))
    linePositions.push(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z)
  }

  lineGeometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3))

  const lineMaterial = new THREE.LineBasicMaterial({
    color: 0x6366f1,
    transparent: true,
    opacity: 0.1
  })

  const lines = new THREE.LineSegments(lineGeometry, lineMaterial)
  scene.add(lines)
}

const animate = () => {
  animationId = requestAnimationFrame(animate)

  if (particles) {
    particles.material.uniforms.time.value += 0.016

    // Slow rotation
    particles.rotation.y += 0.0003
    particles.rotation.x += 0.0001
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