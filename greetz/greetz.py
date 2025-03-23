import colorsys
import math
import random
from math import cos, sin

import pygame
from pygame import gfxdraw


class EnhancedDemoCredits:
    def __init__(self, width=1920, height=1080, fullscreen=False):
        pygame.init()
        self.width = width
        self.height = height

        if fullscreen:
            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption("AI Libraries Evolution - Demo Scene Greetz")
        self.clock = pygame.time.Clock()

        # Credits text with your specific mentions
        self.credits = [
            "GREETZ TO:",
            "Guido van Rossum - Python Creator",
            "PyTorch Crew",
            "TensorFlow Team",
            "LangChain Innovators",
            "Scikit-Learn Pioneers",
            "HuggingFace Transformers Squad",
            "Gource Visualizers",
            "Package Manager UV",
            "--- MUSIC & SFX ---",
            "Elwood",
            "Skaven",
            "florianreichelt",
            "Vincenzo - Project Genesis",
            "SunSpire - Cosmic Potion",
            "--- DEPENDENCIES ---",
            "pydub >= 0.25.1",
            "typer >= 0.15.2",
            "...AND ALL DEMO SCENE REBELS",
            "END OF TRANSMISSION...",
        ]

        # Credit animation parameters
        self.current_credit = 0
        self.credit_timer = 0
        self.credit_fade = 0
        self.credit_y_offset = 0
        self.last_credit = -1  # Track last credit to detect transitions

        # Initialize effects
        self.particles = self.create_particles(200)
        self.explosion_particles = []  # Special particles for explosions
        self.tunnel_offset = 0
        self.tunnel_zoom = 0
        self.time_passed = 0
        self.burst_cooldown = 0  # Cooldown for particle bursts

        # Star field
        self.stars = [
            (random.randint(0, width), random.randint(0, height), random.random() * 2 + 0.5) for _ in range(150)
        ]

        # Font setup
        try:
            self.title_font = pygame.font.Font(None, 80)
            self.font = pygame.font.Font(None, 64)
            self.small_font = pygame.font.Font(None, 32)
        except:
            print("Font loading failed, using default")
            self.title_font = pygame.font.SysFont("arial", 80)
            self.font = pygame.font.SysFont("arial", 64)
            self.small_font = pygame.font.SysFont("arial", 32)

    def create_particles(self, count, explosion=False, x=None, y=None, style=None):
        particles = []
        for _ in range(count):
            # For explosion effects, use the provided center
            if explosion and x is not None and y is not None:
                center_x, center_y = x, y
                # More intense speed for explosions
                speed = random.uniform(3, 15) if explosion else random.uniform(0.5, 3)
                angle = random.uniform(0, 2 * math.pi)
                dx = speed * math.cos(angle)
                dy = speed * math.sin(angle)
                # Larger particle size for explosions
                size = random.uniform(2, 6)
                # Faster fade for explosion particles
                fade_speed = random.uniform(0.01, 0.03)
                # Start fully bright
                lifetime = 1.0
            else:
                # Regular ambient particles
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0.5, 3)
                dx = speed * math.cos(angle)
                dy = speed * math.sin(angle)

                # Starting position near center
                center_x = self.width // 2 + random.randint(-100, 100)
                center_y = self.height // 2 + random.randint(-100, 100)

                # Size and fade parameters
                size = random.uniform(1, 3)
                fade_speed = random.uniform(0.005, 0.02)
                lifetime = 1.0  # Fully bright

            # Particle style (affects color calculation)
            if style is None:
                style = random.choice(["rainbow", "fire", "blue", "green", "gold"])

            particles.append(
                {
                    "x": center_x,
                    "y": center_y,
                    "dx": dx,
                    "dy": dy,
                    "size": size,
                    "fade_speed": fade_speed,
                    "lifetime": lifetime,
                    "style": style,
                    "explosion": explosion,
                    # Add gravity for some particles
                    "gravity": random.uniform(0.05, 0.2) if explosion else 0,
                    # Add rotation for some particles
                    "rotation": random.uniform(-5, 5) if random.random() > 0.7 else 0,
                    # Trail effect
                    "trail": random.random() > 0.5 if explosion else False,
                    # Sparkle effect
                    "sparkle": random.random() > 0.7 if explosion else False,
                }
            )
        return particles

    def create_burst(self, x, y, style=None):
        """Create a particle burst at the specified location"""
        # Determine burst style based on credit content
        if style is None:
            if self.current_credit < len(self.credits):
                text = self.credits[self.current_credit]
                if text.startswith("---"):
                    style = "gold"
                elif text == "GREETZ TO:":
                    style = "rainbow"
                elif text.endswith("..."):
                    style = "fire"
                else:
                    # Regular credits get random style
                    style = random.choice(["rainbow", "blue", "green", "gold"])

        # Create many particles for the burst
        new_particles = self.create_particles(count=random.randint(50, 100), explosion=True, x=x, y=y, style=style)

        # Add them to our explosion particles list
        self.explosion_particles.extend(new_particles)

    def draw_tunnel(self, t):
        # Create tunnel effect using sin/cos patterns with zoom
        zoom = 1 + 0.5 * sin(t / 5)
        for radius in range(50, 500, 20):
            points = []
            num_segments = int(36 + 36 * sin(t / 20))
            for i in range(num_segments):
                angle = i * (2 * math.pi / num_segments)
                distortion = 0.2 * sin(angle * 3 + t / 2)
                mod_radius = radius * (1 + distortion) * zoom

                x = self.width // 2 + int(cos(angle + t / 10) * mod_radius)
                y = self.height // 2 + int(sin(angle + t / 10) * mod_radius)
                points.append((x, y))

            # Draw tunnel rings with gradient colors
            if len(points) > 2:
                # Create pulsing, flowing colors
                hue = (t / 20 + radius / 1000) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.8)
                color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

                # Vary the line width based on time for more dynamic effect
                line_width = max(1, int(2 + sin(t / 3 + radius / 100) * 2))
                pygame.draw.lines(self.screen, color, True, points, line_width)

    def update_particles(self, dt):
        new_particles = []

        # Add some new ambient particles
        if random.random() < 0.3:
            new_particles.extend(self.create_particles(5))

        # Update regular particles
        for p in self.particles:
            # Update position
            p["x"] += p["dx"] * dt * 60
            p["y"] += p["dy"] * dt * 60

            # Update lifetime
            p["lifetime"] -= p["fade_speed"] * dt * 60

            # Keep if still visible and on screen
            if p["lifetime"] > 0 and 0 < p["x"] < self.width and 0 < p["y"] < self.height:
                new_particles.append(p)

        # Limit regular particle count
        if len(new_particles) > 500:
            new_particles = new_particles[:500]

        self.particles = new_particles

        # Handle explosion particles separately
        new_explosion_particles = []
        for p in self.explosion_particles:
            # Apply gravity if needed
            if p["gravity"] > 0:
                p["dy"] += p["gravity"] * dt * 60

            # Apply rotation if needed
            if p["rotation"] != 0:
                angle = math.atan2(p["dy"], p["dx"]) + (p["rotation"] * dt)
                speed = math.hypot(p["dx"], p["dy"])
                p["dx"] = math.cos(angle) * speed
                p["dy"] = math.sin(angle) * speed

            # Update position
            p["x"] += p["dx"] * dt * 60
            p["y"] += p["dy"] * dt * 60

            # Make particles slow down over time
            p["dx"] *= 0.98
            p["dy"] *= 0.98

            # Update lifetime
            p["lifetime"] -= p["fade_speed"] * dt * 60

            # Keep if still visible and on screen
            if (
                p["lifetime"] > 0
                and -50 < p["x"] < self.width + 50  # Allow slight offscreen
                and -50 < p["y"] < self.height + 50
            ):  # for better visual effect
                new_explosion_particles.append(p)

        self.explosion_particles = new_explosion_particles

        # Create bursts on credit transitions
        if self.current_credit != self.last_credit and self.burst_cooldown <= 0:
            # Big burst in the center
            self.create_burst(self.width // 2, self.height // 2)

            # Additional smaller bursts around
            for _ in range(3):
                x = self.width // 2 + random.randint(-200, 200)
                y = self.height // 2 + random.randint(-150, 150)
                self.create_burst(x, y)

            self.burst_cooldown = 10  # Set cooldown to prevent multiple bursts
            self.last_credit = self.current_credit

        # Update burst cooldown
        if self.burst_cooldown > 0:
            self.burst_cooldown -= 1

    def draw_particles(self):
        # Draw regular particles
        for p in self.particles:
            # Calculate brightness based on lifetime
            alpha = int(255 * p["lifetime"])
            size = p["size"]

            # Choose color based on position and time
            dist = math.hypot(p["x"] - self.width / 2, p["y"] - self.height / 2)
            hue = (dist / 500 + self.time_passed / 10) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), alpha)

            # Draw the particle
            gfxdraw.filled_circle(self.screen, int(p["x"]), int(p["y"]), max(1, int(size)), color)

        # Draw explosion particles with special effects
        for p in self.explosion_particles:
            # Calculate brightness based on lifetime
            alpha = int(255 * p["lifetime"])
            size = p["size"] * (1 + 0.5 * (1 - p["lifetime"]))  # Expand as they fade

            # Choose color based on style
            if p["style"] == "rainbow":
                hue = (self.time_passed + p["x"] / self.width) % 1.0
                sat = 0.9
                val = 0.9
            elif p["style"] == "fire":
                # Fire gradient (yellow -> orange -> red)
                hue = 0.05 + (0.08 * (1 - p["lifetime"]))  # Shift from yellow to red
                sat = 0.9
                val = min(1.0, 0.7 + 0.3 * p["lifetime"])
            elif p["style"] == "blue":
                hue = 0.6 + 0.1 * sin(self.time_passed * 5)
                sat = 0.8
                val = 0.9
            elif p["style"] == "green":
                hue = 0.3 + 0.1 * sin(self.time_passed * 5)
                sat = 0.8
                val = 0.9
            elif p["style"] == "gold":
                hue = 0.14 + 0.03 * sin(self.time_passed * 8)
                sat = 0.9
                val = 0.95
            else:
                hue = (self.time_passed / 5) % 1.0
                sat = 0.9
                val = 0.9

            # Apply sparkle effect
            if p["sparkle"] and random.random() < 0.3:
                val = 1.0
                size *= 1.5

            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), alpha)

            # Draw the particle
            px, py = int(p["x"]), int(p["y"])
            radius = max(1, int(size))

            # Draw particle with potentially different shapes
            if random.random() < 0.8 or not p["explosion"]:
                # Regular circle
                gfxdraw.filled_circle(self.screen, px, py, radius, color)

                # Add a highlight in the center for some particles
                if p["explosion"] and p["lifetime"] > 0.7:
                    highlight_color = (255, 255, 255, int(alpha * 0.8))
                    gfxdraw.filled_circle(self.screen, px, py, max(1, radius // 2), highlight_color)
            else:
                # Draw a small line/streak for some particles
                end_x = px + int(p["dx"] * 3)
                end_y = py + int(p["dy"] * 3)
                pygame.draw.line(self.screen, color, (px, py), (end_x, end_y), radius)

            # Add trail for some particles
            if p["trail"] and p["lifetime"] > 0.3:
                trail_x = px - int(p["dx"] * 5)
                trail_y = py - int(p["dy"] * 5)
                for i in range(3):
                    trail_alpha = alpha // (i + 2)
                    trail_color = (color[0], color[1], color[2], trail_alpha)
                    trail_pos_x = px - int(p["dx"] * (i + 1) * 2)
                    trail_pos_y = py - int(p["dy"] * (i + 1) * 2)
                    gfxdraw.filled_circle(self.screen, trail_pos_x, trail_pos_y, max(1, radius - i), trail_color)

    def draw_stars(self, t):
        for i, (x, y, size) in enumerate(self.stars):
            # Make stars twinkle
            brightness = 0.5 + 0.5 * sin(t * 2 + i * 0.1)
            color = (int(200 * brightness), int(200 * brightness), int(255 * brightness))

            # Draw star
            pygame.draw.circle(self.screen, color, (int(x), int(y)), int(size * brightness))

    def draw_current_credit(self, t):
        if self.current_credit < len(self.credits):
            text = self.credits[self.current_credit]

            # Special formatting for section titles
            if text.startswith("---") and text.endswith("---"):
                # Flashing effect for section headers
                flash = sin(t * 10) > 0
                color = (255, 255, 100) if flash else (255, 150, 0)
                text_surface = self.title_font.render(text, True, color)
                # Apply zoom effect
                scale = 1.0 + 0.2 * sin(t * 5)
                size = (int(text_surface.get_width() * scale), int(text_surface.get_height() * scale))
                text_surface = pygame.transform.scale(text_surface, size)
            elif text == "GREETZ TO:":
                # Rainbow color effect for the title
                hue = (t / 2) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
                text_surface = self.title_font.render(text, True, color)
                # Apply zoom effect with rotation
                scale = 1.0 + 0.3 * sin(t * 3)
                size = (int(text_surface.get_width() * scale), int(text_surface.get_height() * scale))
                text_surface = pygame.transform.scale(text_surface, size)
                angle = 5 * sin(t * 2)  # Rotate slightly
                text_surface = pygame.transform.rotate(text_surface, angle)
            elif text.endswith("..."):
                # Dramatic pulsing for ending
                pulse = 0.5 + 0.5 * sin(t * 8)
                text_surface = self.title_font.render(text, True, (255, int(100 * pulse), int(100 * pulse)))
                # Apply dramatic zoom
                scale = 1.0 + 0.5 * pulse
                size = (int(text_surface.get_width() * scale), int(text_surface.get_height() * scale))
                text_surface = pygame.transform.scale(text_surface, size)
            else:
                # More dramatic pulse effect for regular credits
                pulse = 0.6 + 0.4 * sin(t * 8)
                hue = (t / 10 + self.current_credit / len(self.credits)) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                color = (int(rgb[0] * 255 * pulse), int(rgb[1] * 255 * pulse), int(rgb[2] * 255 * pulse))
                text_surface = self.font.render(text, True, color)

                # Apply subtle wave effect
                wave = sin(t * 5 + self.current_credit) * 10
                text_surface = pygame.transform.rotate(text_surface, wave / 2)

            # Credit animation
            alpha = min(255, self.credit_fade)
            text_surface.set_alpha(alpha)

            # Calculate y position with more dramatic bounce effect
            bounce = sin(self.credit_fade / 30) * 40 * (1 - self.credit_fade / 255)
            y_pos = self.height // 2 + int(bounce)

            # Add horizontal movement for more drama
            x_offset = sin(t * 3) * 30

            # Position text
            text_rect = text_surface.get_rect(center=(self.width // 2 + int(x_offset), y_pos))
            self.screen.blit(text_surface, text_rect)

            # Display progress indicator at the bottom
            progress_text = f"{self.current_credit + 1}/{len(self.credits)}"
            progress_surface = self.small_font.render(progress_text, True, (150, 150, 150))
            self.screen.blit(progress_surface, (10, self.height - 40))

    def run(self, duration=30):  # duration in seconds
        start_time = pygame.time.get_ticks()
        last_time = start_time
        running = True

        # Initial particle burst for startup
        self.create_burst(self.width // 2, self.height // 2, style="rainbow")

        while running and (pygame.time.get_ticks() - start_time) < duration * 1000:
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Delta time in seconds
            last_time = current_time
            self.time_passed += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                # Add manual burst trigger on spacebar
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.create_burst(
                        self.width // 2 + random.randint(-200, 200), self.height // 2 + random.randint(-150, 150)
                    )

            # Clear screen with a slight fade for motion blur effect
            fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 25))  # Adjust last value for fade amount
            self.screen.blit(fade_surface, (0, 0))

            # Calculate time value for animations
            t = self.time_passed

            # Draw effects in order
            self.draw_stars(t)
            self.draw_tunnel(t)
            self.update_particles(dt)

            # Random ambient bursts
            if random.random() < 0.03:  # 3% chance per frame
                edge_margin = 100
                x = random.randint(edge_margin, self.width - edge_margin)
                y = random.randint(edge_margin, self.height - edge_margin)
                self.create_burst(x, y)

            # Remember old credit to detect transitions
            old_credit = self.current_credit

            # Credit animation
            if self.credit_fade < 255:
                self.credit_fade += 10  # Faster fade-in
            else:
                self.credit_timer += 1
                if self.credit_timer > 60:  # Show each credit for 1 second (60 frames at 60fps)
                    self.credit_timer = 0
                    self.credit_fade = 0
                    self.current_credit = (self.current_credit + 1) % len(self.credits)

                    # Credit changed - create a special burst when switching
                    if self.current_credit != old_credit:
                        # Main burst at center
                        self.create_burst(self.width // 2, self.height // 2)

                        # Several bursts around the center
                        for _ in range(5):
                            x = self.width // 2 + random.randint(-200, 200)
                            y = self.height // 2 + random.randint(-150, 150)
                            style = random.choice(["rainbow", "fire", "blue", "green", "gold"])
                            self.create_burst(x, y, style)

            # Draw current credit
            self.draw_current_credit(t)

            # Draw particles (on top of text for better effect)
            self.draw_particles()

            # Add a subtle film grain effect
            if random.random() < 0.8:
                for _ in range(100):
                    x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
                    brightness = random.randint(0, 50)
                    self.screen.set_at((x, y), (brightness, brightness, brightness))

            # Calculate and display FPS in the corner for debugging
            fps = self.clock.get_fps()
            fps_text = self.small_font.render(f"FPS: {int(fps)}", True, (100, 100, 100))
            self.screen.blit(fps_text, (self.width - 100, 10))

            # Show remaining time
            time_left = max(0, duration - (current_time - start_time) / 1000)
            time_text = self.small_font.render(f"Time: {int(time_left)}s", True, (100, 100, 100))
            self.screen.blit(time_text, (self.width - 100, 40))

            pygame.display.flip()
            self.clock.tick(60)

        # Create a huge final burst
        for _ in range(10):
            self.create_burst(
                self.width // 2 + random.randint(-300, 300),
                self.height // 2 + random.randint(-200, 200),
                style=random.choice(["fire", "rainbow", "gold"]),
            )

        # Let the particles play out a bit
        for _ in range(60):  # Show burst for 1 second
            self.screen.fill((0, 0, 0, 10), special_flags=pygame.BLEND_RGBA_MULT)
            self.time_passed += 1 / 60
            t = self.time_passed
            self.update_particles(1 / 60)
            self.draw_particles()
            pygame.display.flip()
            self.clock.tick(60)

        # Final fade out
        fade_steps = 30
        for i in range(fade_steps):
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(i * (255 // fade_steps))
            self.screen.blit(fade_surface, (0, 0))

            # Continue updating particles during fade out
            self.time_passed += 1 / 30
            self.update_particles(1 / 30)
            self.draw_particles()

            pygame.display.flip()
            pygame.time.delay(30)

        pygame.quit()


if __name__ == "__main__":
    # You can adjust the resolution or enable fullscreen here
    demo = EnhancedDemoCredits(width=1280, height=720, fullscreen=False)

    # Increased duration to ensure all credits are shown
    # With 20 credits at ~1.2 seconds each (including fade), we need at least 24 seconds
    # Adding some buffer for the final effect
    demo.run(duration=45)
