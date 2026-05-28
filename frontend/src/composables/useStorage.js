import { ref } from 'vue'
import { createClient } from '@supabase/supabase-js'

// Supabase configuration
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

const supabase = supabaseUrl ? createClient(supabaseUrl, supabaseKey) : null

export function useStorage() {
  const uploading = ref(false)
  const uploadProgress = ref(0)
  const uploadError = ref(null)
  const uploadedFiles = ref([])

  const uploadFile = async (file, path = 'uploads') => {
    if (!supabase) {
      uploadError.value = 'Supabase not configured'
      return null
    }

    uploading.value = true
    uploadProgress.value = 0
    uploadError.value = null

    try {
      const fileExt = file.name.split('.').pop()
      const fileName = `${Date.now()}-${Math.random().toString(36).substring(7)}.${fileExt}`
      const filePath = `${path}/${fileName}`

      const { data, error } = await supabase.storage
        .from('amk-ai-storage')
        .upload(filePath, file, {
          cacheControl: '3600',
          upsert: false,
          onUploadProgress: (progress) => {
            uploadProgress.value = Math.round((progress.loaded / progress.total) * 100)
          }
        })

      if (error) throw error

      // Get public URL
      const { data: urlData } = supabase.storage
        .from('amk-ai-storage')
        .getPublicUrl(data.path)

      const uploadedFile = {
        name: file.name,
        path: data.path,
        url: urlData.publicUrl,
        size: file.size,
        type: file.type
      }

      uploadedFiles.value.push(uploadedFile)
      return uploadedFile

    } catch (err) {
      uploadError.value = err.message || 'Upload failed'
      return null
    } finally {
      uploading.value = false
    }
  }

  const uploadMultipleFiles = async (files, path = 'uploads') => {
    const results = []
    for (const file of files) {
      const result = await uploadFile(file, path)
      if (result) {
        results.push(result)
      }
    }
    return results
  }

  const deleteFile = async (path) => {
    if (!supabase) {
      uploadError.value = 'Supabase not configured'
      return false
    }

    try {
      const { error } = await supabase.storage
        .from('amk-ai-storage')
        .remove([path])

      if (error) throw error

      uploadedFiles.value = uploadedFiles.value.filter(f => f.path !== path)
      return true
    } catch (err) {
      uploadError.value = err.message || 'Delete failed'
      return false
    }
  }

  const getSignedUrl = async (path, expiresIn = 3600) => {
    if (!supabase) {
      uploadError.value = 'Supabase not configured'
      return null
    }

    try {
      const { data, error } = await supabase.storage
        .from('amk-ai-storage')
        .createSignedUrl(path, expiresIn)

      if (error) throw error
      return data.signedUrl
    } catch (err) {
      uploadError.value = err.message || 'Failed to get signed URL'
      return null
    }
  }

  const clearFiles = () => {
    uploadedFiles.value = []
    uploadError.value = null
  }

  return {
    uploading,
    uploadProgress,
    uploadError,
    uploadedFiles,
    uploadFile,
    uploadMultipleFiles,
    deleteFile,
    getSignedUrl,
    clearFiles
  }
}