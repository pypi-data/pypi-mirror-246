import torch

def gaussian_directional_envmap(resolution, direction, intensity, alpha, device=None):
  axis_xyz = torch.zeros([6, resolution + 1, resolution + 1, 3], dtype=torch.float32, device=device)
  axis_xyz[0,:,:, 0] = 1.
  axis_xyz[1,:,:, 0] = -1.
  axis_xyz[0:2,:,:, 2] = torch.linspace(-1, 1, resolution + 1, dtype=torch.float32, device=device)[None,:, None]
  axis_xyz[0:2,:,:, 1] = torch.linspace(-1, 1, resolution + 1, dtype=torch.float32, device=device)[None, None,:]
  axis_xyz[2,:,:, 1] = 1.
  axis_xyz[3,:,:, 1] = -1.
  axis_xyz[2:4,:,:, 2] = torch.linspace(-1, 1, resolution + 1, dtype=torch.float32, device=device)[None,:, None]
  axis_xyz[2:4,:,:, 0] = torch.linspace(-1, 1, resolution + 1, dtype=torch.float32, device=device)[None, None,:]
  axis_xyz[4,:,:, 2] = 1.
  axis_xyz[5,:,:, 2] = -1.
  axis_xyz[4:6,:,:, 1] = torch.linspace(-1, 1, resolution + 1, dtype=torch.float32, device=device)[None,:, None]
  axis_xyz[4:6,:,:, 0] = torch.linspace(-1, 1, resolution + 1, dtype=torch.float32, device=device)[None, None,:]
  axis_xyz = (axis_xyz[:, :-1, :-1, ...] + \
              axis_xyz[:, :-1,  1:, ...] + \
              axis_xyz[:,  1:, :-1, ...] + \
              axis_xyz[:,  1:,  1:, ...]) / 4
  axis_xyz = axis_xyz / torch.linalg.norm(axis_xyz, dim=-1, keepdim=True)
  direction = direction / torch.linalg.norm(direction)
  envmap = torch.nn.functional.relu((axis_xyz * direction[None, None, None, :]).sum(dim=-1)).pow(alpha)
  envmap = envmap[None, ...].repeat(3, 1, 1, 1) * intensity[:, None, None, None]
  return envmap
