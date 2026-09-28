# Rea Farms 3D - Blender workflow test

Project: C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D

Arbitrary test geometry only. No source documents were accessed or analyzed.

- Blender: 5.2.2 LTS (C:\Program Files\Blender Foundation\Blender 5.2\blender.exe)
- Modeling: passed: 2 x 2 x 2 meter cube, ground, camera, two area lights
- GPU rendering: passed: Cycles GPU/OPTIX, RTX A1000 only, CPU rendering disabled
- Export: passed: GLB 2.0, two meshes (cube and ground), header validated
- Reopened saved scene: passed
- Reopened cube dimensions in meters: [2.0, 2.0, 2.0]
- Rendering backend: OPTIX
- Render settings: {'resolution': [800, 600], 'max_samples': 32, 'denoising': True, 'denoiser': 'OPTIX'}
- Render duration (wall time, including initialization and denoising): 1.4394 seconds
- Blender process exit code: 0
- Total Blender process duration: 3.3725 seconds

## Detected and enabled Cycles devices

| Device | Backend/type | Enabled | ID |
| --- | --- | --- | --- |
| NVIDIA RTX A1000 | CUDA | False | CUDA_NVIDIA RTX A1000_0000:01:00 |
| Intel Core Ultra 9 285K | CPU | False | CPU |
| NVIDIA RTX A1000 | OPTIX | True | CUDA_NVIDIA RTX A1000_0000:01:00_OptiX |
| Intel(R) Graphics | ONEAPI | False | ONEAPI_Intel(R) oneAPI Unified Runtime over Level-Zero V2_Intel(R) Graphics_0000:00:02.0 |

## GPU evidence

The log records the detected devices, exclusive RTX A1000 OptiX selection, CPU rendering disabled, GPU scene mode, and Cycles diagnostic output. No CPU fallback is implemented. CPU activity for scene preparation or file export is separate from CPU rendering.

```text
DETECTED_DEVICES=[{"name": "NVIDIA RTX A1000", "type": "CUDA", "id": "CUDA_NVIDIA RTX A1000_0000:01:00", "enabled": false}, {"name": "Intel Core Ultra 9 285K", "type": "CPU", "id": "CPU", "enabled": false}, {"name": "NVIDIA RTX A1000", "type": "OPTIX", "id": "CUDA_NVIDIA RTX A1000_0000:01:00_OptiX", "enabled": false}, {"name": "Intel(R) Graphics", "type": "ONEAPI", "id": "ONEAPI_Intel(R) oneAPI Unified Runtime over Level-Zero V2_Intel(R) Graphics_0000:00:02.0", "enabled": false}]
ENABLED_DEVICES=[{"name": "NVIDIA RTX A1000", "type": "CUDA", "id": "CUDA_NVIDIA RTX A1000_0000:01:00", "enabled": false}, {"name": "Intel Core Ultra 9 285K", "type": "CPU", "id": "CPU", "enabled": false}, {"name": "NVIDIA RTX A1000", "type": "OPTIX", "id": "CUDA_NVIDIA RTX A1000_0000:01:00_OptiX", "enabled": true}, {"name": "Intel(R) Graphics", "type": "ONEAPI", "id": "ONEAPI_Intel(R) oneAPI Unified Runtime over Level-Zero V2_Intel(R) Graphics_0000:00:02.0", "enabled": false}]
RENDER_CONFIG={"engine": "CYCLES", "backend": "OPTIX", "device": "GPU", "resolution": [800, 600], "samples": 32, "denoising": true, "denoiser": "OPTIX"}
00:01.453  cycles           | WARNING Could not create directory: "C:\Users\Brandon\AppData\Local/NVIDIA/OptixCache" Storing optix7cache.db in the current working directory.
00:02.125  cycles           | Using fast to trace OptiX BVH
00:02.125  cycles           | Using fast to trace OptiX BVH
00:02.125  cycles           | Using OPTIX layout.
00:02.125  cycles           | Using fast to trace OptiX BVH
                            | Path tracing on: NVIDIA RTX A1000 (OptiX) [CUDA_NVIDIA RTX A1000_0000:01:00_OptiX]
                            | Denoising on: NVIDIA RTX A1000 (OptiX) [CUDA_NVIDIA RTX A1000_0000:01:00_OptiX]
                            |   Type: OptiX
```

## Outputs

- script: C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\scripts\blender_test_v002.py (17698 bytes)
- blend: C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\models\blender_test_v002.blend (99253 bytes)
- png: C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\renders\blender_test_v002.png (415049 bytes)
- glb: C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\exports\blender_test_v002.glb (3000 bytes)
- report: C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\notes\blender_test_v002.md (this report)
- log: C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\notes\blender_test_v002.log (11748 bytes)

## Script exceptions

```text
None
```

## Reuse

Run this script with the Python bundled with Blender. It chooses the next unused version across all six outputs and copies itself to that version. It refuses to overwrite outputs.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\5.2\python\bin\python.exe' 'C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\scripts\blender_test_v002.py'
```

Preferences are changed only in the child process. No global preferences or startup file are saved. The GLB uses Blender's bundled exporter. No add-ons, software, or assets are installed or downloaded.

## Single next step

Review the rendered test image. No building modeling has begun.

## Verified GPU execution

- Cycles explicitly names RTX A1000 OptiX for path tracing: True
- Cycles explicitly names RTX A1000 OptiX for denoising: True
- GPU evidence: confirmed

## Console warnings and errors

~~~text
00:01.282  cycles           | WARNING HIPEW initialization failed: Error opening HIP dynamic library
C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\scripts\blender_test_v002.py:102: DeprecationWarning: 'Material.use_nodes' is expected to be removed in Blender 6.0
00:01.453  cycles           | WARNING Could not create directory: "C:\Users\Brandon\AppData\Local/NVIDIA/OptixCache" Storing optix7cache.db in the current working directory.
00:02.782  image.write      | ERROR OpenImageIO write failed: Could not open file "\.thumbnails\large\blender_3296_93a5dec0a0257f82d6634ce3d0f5e263.png.png"
~~~

Console diagnostics are retained even when Blender exits successfully. A failed thumbnail write concerns Blender's file thumbnail, not the requested render PNG. Detection of unavailable HIP does not affect the selected OptiX backend.

## Incidental runtime files

Blender runs in C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\notes\blender_test_v002_runtime so any fallback OptiX cache stays separate from previous runs. No prior cache file is overwritten.
The earlier v001 outputs are preserved. This revision adds complete console diagnostic reporting.

## Completion checks

- script: exists=True, bytes=17698
- blend: exists=True, bytes=99253
- png: exists=True, bytes=415049
- glb: exists=True, bytes=3000
- log: exists=True, bytes=11748
