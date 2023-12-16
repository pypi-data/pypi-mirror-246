"""
Screen renderable items for pygame-based simulation visualization
"""

import os
import param

from ..param import (Viewable, PositiveNumber, ViewableToggleable, NestedConf, PositiveInteger, Area2DPixel,
                     PosPixelRel2Area, NumericTuple2DRobust, Pos2D, IntegerTuple)

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

__all__ = [
    'IDBox',
    'ScreenTextBoxRect',
    'ScreenMsgText',
    'ScreenTextBox',
    'SimulationClock',
    'SimulationScale',
    'SimulationState',
]


# class ScreenArea(Area2DPixel):
#     # manager  = param.ClassSelector(_class=)
#
#     def __init__(self, manager, **kwargs):
#         self.manager = manager
#         super().__init__(dims=aux.get_window_dims(self.space.dims), **kwargs)
#
#     @property
#     def space(self):
#         return self.manager.model.space
#
#     @property
#     def scaling_factor(self):
#         return self.manager.model.scaling_factor
#
#     def space2screen_pos(self, pos):
#         return self.manager.space2screen_pos(pos)
#
#
#
#
#
#
#
#
# class ScreenAreaZoomable(ScreenArea):
#     zoom = PositiveNumber(1., doc='Zoom factor')
#     center = param.Parameter(np.array([0., 0.]), doc='Center xy')
#     center_lim = param.Parameter(np.array([0., 0.]), doc='Center xy lim')
#     _scale = param.Parameter(np.array([[1., .0], [.0, -1.]]), doc='Scale of xy')
#     _translation = param.Parameter(np.zeros(2), doc='Translation of xy')
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.set_bounds()
#
#     @property
#     def display_size(self):
#         return (np.array(self.dims) / self.zoom).astype(int)
#
#     @param.depends('zoom', 'center', watch=True)
#     def set_bounds(self):
#         s, z = self.scaling_factor, self.zoom
#         rw, rh = self.w / self.space.w, self.h / self.space.h
#         # left, right, bottom, top=self.space.range * s
#         # assert right > left and top > bottom
#         # x = int(self.w/ z) / (self.space.w* s)
#         # y = int(self.h/ z) / (self.space.h* s)
#         self._scale = np.array([[rw, .0], [.0, -rh]]) / z / s
#         self._translation = np.array(self.dims) / 2 + self.center / z / s * [-rw, rh]
#         self.center_lim = (z - 1) * s * np.array(self.space.dims) / 2
#
#     def _transform(self, position):
#         return np.round(self._scale.dot(position) + self._translation).astype(int)
#
#     def move_center(self, dx=0, dy=0, pos=None):
#         if pos is None:
#             pos = self.center - self.center_lim * [dx, dy]
#         self.center = np.clip(pos, self.center_lim, -self.center_lim)
#
#     def zoom_screen(self, sign, pos=None):
#         d_zoom = -0.01 * sign
#         if pos is None:
#             pos = self.mouse_position
#         if 0.001 <= self.zoom + d_zoom <= 1:
#             self.zoom = np.round(self.zoom + d_zoom, 2)
#             self.center = np.clip(self.center - np.array(pos) * d_zoom, self.center_lim, -self.center_lim)
#         if self.zoom == 1.0:
#             self.center = np.array([0.0, 0.0])
#
#     @param.depends('zoom', watch=True)
#     def update_scale(self):
#         def closest(lst, k):
#             return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - k))]
#
#         def compute_lines(x, y, scale):
#             return [[(x - scale / 2, y), (x + scale / 2, y)],
#                     [(x + scale / 2, y * 0.75), (x + scale / 2, y * 1.25)],
#                     [(x - scale / 2, y * 0.75), (x - scale / 2, y * 1.25)]]
#
#         w_in_mm = self.space.w * self.zoom * 1000
#         # Get 1/10 of max real dimension, transform it to mm and find the closest reasonable scale
#         scale_in_mm = closest(
#             lst=[0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10, 25, 50, 75, 100, 250, 500, 750, 1000], k=w_in_mm / 10)
#         self.text_font.set_text(f'{scale_in_mm} mm')
#         self.lines = compute_lines(self.x, self.y, scale_in_mm / w_in_mm * self.w)
#
#
# class ScreenAreaPygame(ScreenAreaZoomable):
#     caption = param.String('', doc='The caption of the screen window')
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         pygame.init()
#         os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1550, 400)
#         self._window = self.init_screen()
#         # self._t = pygame.time.Clock()
#
#         if self.manager.bg is not None:
#             self.set_background()
#         else:
#             self.bgimage = None
#             self.bgimagerect = None
#
#     @property
#     def mouse_position(self):
#
#         p = np.array(pygame.mouse.get_pos()) - self._translation
#         return np.linalg.inv(self._scale).dot(p)
#
#     @property
#     def new_display_surface(self):
#         return pygame.Surface(self.display_size, pygame.SRCALPHA)
#
#     def draw_arena(self, tank_color, screen_color):
#         surf1 = self.new_display_surface
#         surf2 = self.new_display_surface
#         vs = [self._transform(v) for v in self.space.vertices]
#         pygame.draw.polygon(surf1, tank_color, vs, 0)
#         pygame.draw.rect(surf2, screen_color, surf2.get_rect())
#         surf2.blit(surf1, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
#         self._window.blit(surf2, (0, 0))
#
#     def init_screen(self):
#         flags = pygame.HWSURFACE | pygame.DOUBLEBUF
#         if self.manager.show_display:
#             window = pygame.display.set_mode((self.w + self.manager.panel_width, self.h), flags)
#             pygame.display.set_caption(self.caption)
#             pygame.event.set_allowed(pygame.QUIT)
#         else:
#             window = pygame.Surface(self.display_size, flags)
#         return window
#
#     def draw_circle(self, position=(0, 0), radius=.1, color=(0, 0, 0), filled=True, width=.01):
#         p = self._transform(position)
#         r = int(self._scale[0, 0] * radius)
#         w = 0 if filled else int(self._scale[0, 0] * width)
#         pygame.draw.circle(self._window, color, p, r, w)
#
#     def draw_polygon(self, vertices, color=(0, 0, 0), filled=True, width=.01):
#         if vertices is not None and len(vertices) > 1:
#             vs = [self._transform(v) for v in vertices]
#             w = 0 if filled else int(self._scale[0, 0] * width)
#             pygame.draw.polygon(self._window, color, vs, w)
#
#     def draw_convex(self, points, **kwargs):
#         from scipy.spatial import ConvexHull
#
#         ps = np.array(points)
#         vs = ps[ConvexHull(ps).vertices].tolist()
#         self.draw_polygon(vs, **kwargs)
#
#     def draw_grid(self, all_vertices, colors, filled=True, width=.01):
#         all_vertices = [[self._transform(v) for v in vertices] for vertices in all_vertices]
#         w = 0 if filled else int(self._scale[0, 0] * width)
#         for vs, c in zip(all_vertices, colors):
#             pygame.draw.polygon(self._window, c, vs, w)
#
#     def draw_polyline(self, vertices, color=(0, 0, 0), closed=False, width=.01):
#         vs = [self._transform(v) for v in vertices]
#         w = int(self._scale[0, 0] * width)
#         if isinstance(color, list):
#             for v1, v2, c in zip(vs[:-1], vs[1:], color):
#                 pygame.draw.lines(self._window, c, closed=closed, points=[v1, v2], width=w)
#         else:
#             pygame.draw.lines(self._window, color, closed=closed, points=vs, width=w)
#
#     def draw_line(self, start, end, color=(0, 0, 0), width=.01):
#         start = self._transform(start)
#         end = self._transform(end)
#         w = int(self._scale[0, 0] * width)
#         pygame.draw.line(self._window, color, start, end, w)
#
#     def draw_transparent_circle(self, position=(0, 0), radius=.1, color=(0, 0, 0, 125), filled=True, width=.01):
#         r = int(self._scale[0, 0] * radius)
#         s = pygame.Surface((2 * r, 2 * r), pygame.HWSURFACE | pygame.SRCALPHA)
#         w = 0 if filled else int(self._scale[0, 0] * width)
#         pygame.draw.circle(s, color, (r, r), radius, w)
#         self._window.blit(s, self._transform(position) - r)
#
#     def draw_text_box(self, font, rect):
#         self._window.blit(font, rect)
#
#     def draw_envelope(self, points, **kwargs):
#         vs = list(geometry.MultiPoint(points).envelope.exterior.coords)
#         self.draw_polygon(vs, **kwargs)
#
#     def draw_arrow_line(self, start, end, color=(0, 0, 0), width=.01, dl=0.02, phi=0, s=10):
#         a0 = math.atan2(end[1] - start[1], end[0] - start[0])
#         l0 = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
#         w = int(self._scale[0, 0] * width)
#         pygame.draw.line(self._window, color, self._transform(start), self._transform(end), w)
#
#         a = a0 + np.pi / 2
#         sin0, cos0 = math.sin(a) * s, math.cos(a) * s
#         sin1, cos1 = math.sin(a - np.pi * 2 / 3) * s, math.cos(a - np.pi * 2 / 3) * s
#         sin2, cos2 = math.sin(a + np.pi * 2 / 3) * s, math.cos(a + np.pi * 2 / 3) * s
#
#         l = 0 + phi * dl
#         while l < l0:
#             pos = self._transform((start[0] + math.cos(a0) * l, start[1] + math.sin(a0) * l))
#             p0 = (pos[0] + sin0, pos[1] + cos0)
#             p1 = (pos[0] + sin1, pos[1] + cos1)
#             p2 = (pos[0] + sin2, pos[1] + cos2)
#             pygame.draw.polygon(self._window, color, (p0, p1, p2))
#             l += dl
#
#     def set_background(self):
#         # if self.bg is not None:
#         ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#         path = os.path.join(ROOT_DIR, 'background.png')
#         print('Loading background image from', path)
#         self.bgimage = pygame.image.load(path)
#         self.bgimagerect = self.bgimage.get_rect()
#         self.tw = self.bgimage.get_width()
#         self.th = self.bgimage.get_height()
#         self.th_max = int(self._window.get_height() / self.th) + 2
#         self.tw_max = int(self._window.get_width() / self.tw) + 2
#
#     def draw_background(self, bg=[0, 0, 0]):
#         if self.bgimage is not None and self.bgimagerect is not None:
#             x, y, a = bg
#             try:
#                 min_x = int(np.floor(x))
#                 min_y = -int(np.floor(y))
#
#                 for py in np.arange(min_y - 1, self.th_max + min_y, 1):
#                     for px in np.arange(min_x - 1, self.tw_max + min_x, 1):
#                         if a != 0.0:
#                             pass
#                         p = ((px - x) * (self.tw - 1), (py + y) * (self.th - 1))
#                         self._window.blit(self.bgimage, p)
#             except:
#                 pass
#
#
# class Viewer(ScreenAreaPygame):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.vid_writer = self.manager.new_video_writer(fps=self.manager._fps)
#         self.img_writer = self.manager.new_image_writer()
#
#     def render(self):
#         if self.manager.show_display:
#             pygame.display.flip()
#             image = pygame.surfarray.pixels3d(self._window)
#             # self._t.tick(self.manager._fps)
#         else:
#             image = pygame.surfarray.array3d(self._window)
#         if self.vid_writer:
#             self.vid_writer.append_data(np.flipud(np.rot90(image)))
#         if self.img_writer:
#             self.img_writer.append_data(np.flipud(np.rot90(image)))
#             self.img_writer = None
#         return image
#
#     @staticmethod
#     def close_requested():
#         if pygame.display.get_init():
#             return pygame.event.peek(pygame.QUIT)
#         return False
#
#     def close(self):
#         pygame.display.quit()
#         if self.vid_writer:
#             self.vid_writer.close()
#         if self.img_writer:
#             self.img_writer.close()
#         del self
#
#         reg.vprint('Screen closed', 1)


class ScreenTextFont(NestedConf):
    text_color = param.Color('black', doc='The color of the text')
    text = param.String('', doc='The text to draw')
    font_size = PositiveInteger(20, doc='The font size')
    font_type = param.Parameter("Trebuchet MS", doc='The font type to use')
    text_centre = NumericTuple2DRobust(doc='The text center position')

    def __init__(self, end_time=0, start_time=0, **kwargs):
        self.font = None
        self.text_font = None
        self.text_font_r = None
        super().__init__(**kwargs)
        self.end_time = end_time
        self.start_time = start_time
        if not self.font:
            self.update_font()

    @param.depends('text', 'text_color', 'text_centre', watch=True)
    def render_text(self):
        if not self.font:
            self.update_font()
        if self.N_text_lines == 1:
            self.text_font = self.font.render(self.text, 1, self.text_color)  # zero-pad hours to 2 digits
            self.text_font_r = self.text_font.get_rect()
            self.text_font_r.center = self.text_centre
        else:
            N = self.N_text_lines
            ls = self.text_lines
            self.text_font = []
            self.text_font_r = []
            x0, y0 = self.text_centre
            for i in range(N):
                f = self.font.render(ls[i], True, self.text_color)
                r = f.get_rect()
                r.center = x0, y0 + (i - int(N / 2)) * 50
                self.text_font.append(f)
                self.text_font_r.append(r)

    @property
    def text_lines(self):
        return self.text.splitlines()

    @property
    def N_text_lines(self):
        return len(self.text_lines)

    @param.depends('font_size', watch=True)
    def update_font(self):
        pygame.init()
        self.font = pygame.font.SysFont(self.font_type, self.font_size)

    def draw(self, v, **kwargs):
        if self.text_font is None or self.text_font_r is None:
            self.render_text()
        if self.N_text_lines == 1:
            v.draw_text_box(self.text_font, self.text_font_r)
        else:
            for i in range(self.N_text_lines):
                v.draw_text_box(self.text_font[i], self.text_font_r[i])

    def set_text(self, text):
        self.text = text

    def flash_text(self, text, t=2):
        self.set_text(text)
        self.end_time = pygame.time.get_ticks() + t * 1000
        self.start_time = pygame.time.get_ticks() + int(0.1 * 1000)


class ScreenTextFontRel(ScreenTextFont):
    text_centre_scale = param.NumericTuple((0.9, 0.9),
                                           # text_centre_scale = PositiveRange((0.9, 0.9), softmax=10.0, step=0.01,
                                           doc='The text center position relative to the position')
    font_size_scale = PositiveNumber(1 / 40, doc='The font size relative to the window size')
    reference_object = param.ClassSelector(class_=PosPixelRel2Area, doc='The object hosting the text')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_font_size(self.reference_object)
        self.update_font_centre_pos(self.reference_object)

    @param.depends('reference_object.pos', 'text_centre_scale', watch=True)
    def update_font_centre_pos(self, obj):
        dx, dy = self.text_centre_scale
        self.text_centre = (obj.x * dx, obj.y * dy)

    # @param.depends('reference_object', watch=True)
    def update_font_size(self, obj):
        self.font_size = int(obj.reference_area.w * self.font_size_scale)


class ScreenTextBoxRect(ScreenTextFont, Viewable):
    visible = param.Boolean(False)
    frame_rect = param.ClassSelector(class_=pygame.Rect, doc='The frame rectangle')
    linewidth = PositiveNumber(10.0, doc='The linewidth to draw the box')
    show_frame = param.Boolean(True, doc='Draw the rectangular frame around the text')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_centre = self.frame_rect.center

    def draw(self, v, **kwargs):
        if self.show_frame and self.frame_rect is not None:
            pygame.draw.rect(v._window, color=self.text_color, rect=self.frame_rect, width=int(self.linewidth))

        super().draw(v=v, **kwargs)


class ScreenTextBox(ScreenTextFont, ViewableToggleable, Area2DPixel):
    dims = IntegerTuple(default=(140, 32))
    visible = param.Boolean(False)
    linewidth = PositiveNumber(0.001, doc='The linewidth to draw the box')
    show_frame = param.Boolean(True, doc='Draw the rectangular frame around the text')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame_rect = None

    def set_frame_rect(self, pos=None, **kwargs):
        return self.get_rect_at_pos(pos, **kwargs)

    def draw(self, v, **kwargs):
        if self.show_frame:
            if self.frame_rect is not None:
                # v.draw_polygon(self.shape, color=self.color, filled=False, width=self.linewidth)
                # pygame.draw.rect(v._window, color=self.color, rect=self.shape)
                pygame.draw.rect(v._window, color=self.color, rect=self.frame_rect,
                                 width=int(v._scale[0, 0] * self.linewidth))


class IDBox(ScreenTextFont, ViewableToggleable):
    visible = param.Boolean(False)
    agent = param.ClassSelector(class_=Pos2D, doc='The agent owning the ID')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_font()
        self.update_agent()

    def update_agent(self):
        self.text_color = self.agent.color
        self.set_text(self.agent.unique_id)

    # @param.depends('agent.pos', watch=True)
    def update_font_centre_pos(self, v):
        pos = self.agent.get_position()
        x, y = v.space2screen_pos(pos)
        self.text_centre = x + 50, y + 12

    def draw(self, v, **kwargs):
        self.update_font_centre_pos(v)
        self.update_agent()
        ScreenTextFont.draw(self, v=v, **kwargs)


class PosPixelRel2AreaViewable(PosPixelRel2Area, Viewable): pass


class ScreenMsgText(ScreenTextFontRel, Viewable):
    text_centre_scale = param.NumericTuple((0.91, 1), doc='The text center position relative to the position')
    font_size_scale = PositiveNumber(1 / 25, doc='The font size relative to the window size')
    font_type = param.Parameter(default="SansitaOne.tff")

    def __init__(self, reference_area, **kwargs):
        reference_object = PosPixelRel2Area(reference_area=reference_area,
                                            pos_scale=(0.95, 0.1))
        super().__init__(reference_object=reference_object, **kwargs)

    def draw(self, v, **kwargs):
        ScreenTextFont.draw(self, v=v, **kwargs)
        # self.text_font.draw(v, **kwargs)

    def set_default_color(self, color):
        super().set_default_color(color)
        self.text_color = self.color


class SimulationClock(PosPixelRel2AreaViewable):
    pos_scale = param.NumericTuple((0.94, 0.04))

    def __init__(self, sim_step_in_sec, **kwargs):
        super().__init__(**kwargs)
        # Time Info
        self.sim_step_in_dms = int(sim_step_in_sec * 100)
        self.time_in_min = 0
        self.dmsecond = 0
        self.second = 0
        self.minute = 0
        self.hour = 0

        kws = {
            'reference_object': self,
            'text_color': self.color,
        }

        self.text_fonts = {
            'hour': ScreenTextFontRel(font_size_scale=(1 / 40), text_centre_scale=(0.91, 1.0), **kws),
            'minute': ScreenTextFontRel(font_size_scale=(1 / 40), text_centre_scale=(0.95, 1.0), **kws),
            'second': ScreenTextFontRel(font_size_scale=(1 / 50), text_centre_scale=(1.0, 1.0), **kws),
            'dmsecond': ScreenTextFontRel(font_size_scale=(1 / 50), text_centre_scale=(1.04, 1.1), **kws),
        }

    def tick_clock(self):
        # self.counter += 1
        self.dmsecond += self.sim_step_in_dms
        if self.dmsecond >= 100:
            self.second += 1
            self.dmsecond -= 100
            if self.second >= 60:
                self.minute += 1
                self.second -= 60
                if self.minute >= 60:
                    self.hour += 1
                    self.minute -= 60

    def draw(self, v, **kwargs):
        for k, f in self.text_fonts.items():
            t = getattr(self, k)
            if k != 'hour':
                f.set_text(":{0:02}".format(t))
            else:
                f.set_text("{0:02}".format(t))
            f.draw(v, **kwargs)

    def set_default_color(self, color):
        super().set_default_color(color)
        for k, v in self.text_fonts.items():
            v.text_color = self.color


class SimulationScale(PosPixelRel2AreaViewable):
    pos_scale = param.NumericTuple((0.1, 0.04))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kws = {
            'reference_object': self,
            'text_color': self.color,
        }
        self.text_font = ScreenTextFontRel(font_size_scale=(1 / 40), text_centre_scale=(1, 1.5), **kws)

        self.lines = None
        self.update_scale()

    @param.depends('reference_area.zoom', watch=True)
    def update_scale(self):
        def closest(lst, k):
            return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - k))]

        w_in_mm = self.reference_area.model.space.w * self.reference_area.zoom * 1000
        # Get 1/10 of max real dimension, transform it to mm and find the closest reasonable scale
        self.scale_in_mm = closest(
            lst=[0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10, 25, 50, 75, 100, 250, 500, 750, 1000], k=w_in_mm / 10)
        self.text_font.set_text(f'{self.scale_in_mm} mm')
        self.lines = self.compute_lines(self.x, self.y, self.scale_in_mm / w_in_mm * self.reference_area.w)

    def compute_lines(self, x, y, scale):
        return [[(x - scale / 2, y), (x + scale / 2, y)],
                [(x + scale / 2, y * 0.75), (x + scale / 2, y * 1.25)],
                [(x - scale / 2, y * 0.75), (x - scale / 2, y * 1.25)]]

    def draw(self, v, **kwargs):
        for line in self.lines:
            pygame.draw.line(v._window, self.color, line[0], line[1], 1)
        # v.draw_text_box(self.text_font, self.text_font_r)
        self.text_font.draw(v, **kwargs)

    def set_default_color(self, color):
        super().set_default_color(color)
        self.text_font.text_color = self.color


class SimulationState(PosPixelRel2AreaViewable):
    pos_scale = param.NumericTuple((0.85, 0.94))

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        kws = {
            'reference_object': self,
            'text_color': self.color,
        }
        self.text_font = ScreenTextFontRel(font_size_scale=(1 / 40), text_centre_scale=(1, 1), **kws)

    def set_text(self, text):
        self.text_font.set_text(text)

    def draw(self, v, **kwargs):
        self.text_font.draw(v, **kwargs)

    def set_default_color(self, color):
        super().set_default_color(color)
        self.text_font.text_color = self.color
