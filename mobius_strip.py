import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson as simps

class MobiusStrip:
    def __init__(self, R=1.0, w=0.2, n=100):
        """
        Initialize Mobius strip parameters and compute mesh grids.
        
        Parameters:
        R : float - Radius of the central circle
        w : float - Width of the strip
        n : int   - Resolution (number of points along each parameter)
        """
        self.R = R
        self.w = w
        self.n = n
        
        # Parameter ranges
        self.u = np.linspace(0, 2 * np.pi, n)          # Along length of strip
        self.v = np.linspace(-w / 2, w / 2, n)         # Across width of strip
        
        # Create 2D parameter grids for mesh
        self.U, self.V = np.meshgrid(self.u, self.v)
        
        # Compute the 3D coordinates of the surface points
        self.X, self.Y, self.Z = self.compute_mesh()

    def compute_mesh(self):
        """
        Compute 3D coordinates (X, Y, Z) of the Mobius strip surface mesh
        based on parametric equations.
        """
        U, V = self.U, self.V
        X = (self.R + V * np.cos(U / 2)) * np.cos(U)
        Y = (self.R + V * np.cos(U / 2)) * np.sin(U)
        Z = V * np.sin(U / 2)
        return X, Y, Z

    def compute_surface_area(self):
        """
        Approximate the surface area of the Mobius strip by computing 
        the magnitude of the cross product of partial derivatives and
        integrating over the parameter space using Simpson's rule.
        """
        # Partial derivatives w.r.t. u and v
        dXdu = np.gradient(self.X, axis=1)
        dYdu = np.gradient(self.Y, axis=1)
        dZdu = np.gradient(self.Z, axis=1)
        
        dXdv = np.gradient(self.X, axis=0)
        dYdv = np.gradient(self.Y, axis=0)
        dZdv = np.gradient(self.Z, axis=0)
        
        # Compute cross product of derivatives at each point (surface normal magnitude)
        cross_prod = np.cross(
            np.stack((dXdu, dYdu, dZdu), axis=-1),
            np.stack((dXdv, dYdv, dZdv), axis=-1)
        )
        
        # Area elements magnitude
        area_elements = np.linalg.norm(cross_prod, axis=-1)
        
        # Double integral over parameter grid using Simpson's rule
        area = simps(simps(area_elements, self.v), self.u)
        return area

    def compute_edge_length(self):
        """
        Compute the length of one edge of the Mobius strip by evaluating
        the curve at v = +w/2 and summing distances between successive points.
        """
        u_edge = self.u
        v_edge = self.w / 2 * np.ones_like(u_edge)
        
        # Parametric equations of the edge curve
        x_edge = (self.R + v_edge * np.cos(u_edge / 2)) * np.cos(u_edge)
        y_edge = (self.R + v_edge * np.cos(u_edge / 2)) * np.sin(u_edge)
        z_edge = v_edge * np.sin(u_edge / 2)
        
        # Differences between consecutive points
        dx = np.gradient(x_edge)
        dy = np.gradient(y_edge)
        dz = np.gradient(z_edge)
        
        # Euclidean distances between points
        edge_lengths = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # Sum to get total edge length
        return np.sum(edge_lengths)

    def plot(self):
        """
        Plot the Mobius strip surface in 3D using matplotlib.
        """
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.plot_surface(
            self.X, self.Y, self.Z,
            cmap='viridis',          # Smooth colormap for surface
            edgecolor='k',           # Black grid lines
            linewidth=0.2
        )
        
        ax.set_title("Möbius Strip")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        
        plt.tight_layout()
        plt.show()

def main():
    try:
        # User inputs for parameters
        R = float(input("Enter the radius R (e.g. 1.0): "))
        w = float(input("Enter the width w (e.g. 0.2): "))
        n = int(input("Enter the resolution n (e.g. 200): "))
        
        mobius = MobiusStrip(R=R, w=w, n=n)
        
        # Compute and display properties
        surface_area = mobius.compute_surface_area()
        edge_length = mobius.compute_edge_length()
        
        print(f"\nComputed Properties:")
        print(f"Surface Area: {surface_area:.5f}")
        print(f"Edge Length: {edge_length:.5f}")
        
        # Visualize
        mobius.plot()
    
    except ValueError:
        print("Invalid input. Please enter numeric values for R, w, and n.")

if __name__ == "__main__":
    main()
