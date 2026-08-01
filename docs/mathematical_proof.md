# Mathematical Proof: 6-Vector Tensor Field Derivations

**Document ID:** MP-6V-2026-02  
**Subject:** Formal Derivation of Instantaneous Tracking Angle ($\theta_i$) and Zero-Shear Dynamic Equilibrium

---

## 1. Local Stress Tensor Definition

Consider an autonomous body fully immersed in a continuous 3D fluid medium. At any instantaneous coordinate $(x, y, z)$, the localized stress field acting on the vehicle's boundary interface is defined by the symmetric 2nd-order stress tensor $\boldsymbol{\sigma}$:

$$\boldsymbol{\sigma} = \begin{bmatrix} 
\sigma_{xx} & \tau_{xy} & \tau_{xz} \\ 
\tau_{xy} & \sigma_{yy} & \tau_{yz} \\ 
\tau_{xz} & \tau_{yz} & \sigma_{zz} 
\end{bmatrix}$$

Extracting the 6 independent spatial components yields the local state vector $\mathbf{S} \in \mathbb{R}^6$:

$$\mathbf{S} = \begin{bmatrix} \sigma_{xx} & \sigma_{yy} & \sigma_{zz} & \tau_{xy} & \tau_{yz} & \tau_{zx} \end{bmatrix}^T$$

---

## 2. Shear Strain Energy Minimization

To achieve **Zero (Dynamic Equilibrium)**, the vehicle must orient its longitudinal primary axis along the trajectory that minimizes net shear resistance. The total shear strain energy density $W_s$ stored along the primary horizontal operational plane $(x-y)$ is given by:

$$W_s(\theta) = \tau_{xy}'^2 = \left( -\frac{\sigma_{xx} - \sigma_{yy}}{2} \sin(2\theta) + \tau_{xy} \cos(2\theta) \right)^2$$

To find the stationary points where shear stress vanishes ($\tau_{xy}' = 0$), we set the inner shear expression to zero:

$$-\frac{\sigma_{xx} - \sigma_{yy}}{2} \sin(2\theta_i) + \tau_{xy} \cos(2\theta_i) = 0$$

Rearranging terms yields:

$$\frac{\sin(2\theta_i)}{\cos(2\theta_i)} = \tan(2\theta_i) = \frac{2 \tau_{xy}}{\sigma_{xx} - \sigma_{yy}}$$

---

## 3. Instantaneous Tracking Angle ($\theta_i$) Resolution

Applying the four-quadrant inverse tangent function ($\text{arctan2}$) to handle all directional force signs and avoid zero-division singularities gives:

$$2\theta_i = \text{arctan2}\left(2\tau_{xy}, \, \sigma_{xx} - \sigma_{yy}\right)$$

$$\theta_i = \frac{1}{2} \text{arctan2}\left(2\tau_{xy}, \, \sigma_{xx} - \sigma_{yy}\right) + \phi_{\text{trim}}$$

Where $\phi_{\text{trim}}$ accounts for fixed structural hull geometry offsets.

---

## 4. Equilibrium Condition & Convergence Criteria

Dynamic equilibrium is achieved when the residual shear magnitude $|\boldsymbol{\tau}_{\text{res}}|$ satisfies:

$$|\boldsymbol{\tau}_{\text{res}}| = \sqrt{\tau_{xy}'^2 + \tau_{yz}'^2 + \tau_{zx}'^2} \le \varepsilon$$

Where $\varepsilon \to 0$ represents the noise floor of the physical strain-sensor system. When this condition holds, external fluid motion does not displace the body off-path, but rather propels it along its resolved equilibrium vector with zero rotational torque.
