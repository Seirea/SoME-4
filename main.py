from manim.animation.speedmodifier import ChangeSpeed
from manim.utils.color.manim_colors import ORANGE
from manim.mobject.value_tracker import ValueTracker
from manim.constants import RIGHT
from video import Cyclotomics
from manim.utils.color.manim_colors import YELLOW
from manim.mobject.geometry.arc import Dot
from manim.mobject.graphing.coordinate_systems import ComplexPlane
from manim.constants import PI
from manim.mobject.types.vectorized_mobject import VGroup
from manim.animation.indication import Blink
from manim.mobject.geometry.polygram import Rectangle
from manim.utils.color.manim_colors import GREY_A
from manim.animation.creation import TypeWithCursor
from manim.mobject.svg.brace import BraceLabel
from typing import Callable
from manim.animation.animation import Animation
from manim.animation.creation import Create
from manim.mobject.geometry.shape_matchers import SurroundingRectangle
from manim.animation.growing import GrowArrow
from manim.mobject.geometry.line import Arrow
from manim.mobject.mobject import Mobject
from manim.animation.transform import ReplacementTransform
from manim.mobject.text.tex_mobject import MathTex
from manim.animation.transform import Restore
import manim
from manim import Scene, Text, Tex, Write, Unwrite, FadeOut, DOWN, UP, LEFT, Transform, FadeIn, ReplacementTransform
import numpy as np

# class SectionDisplay(Tex):


# Aliases
mt = MathTex
tx = Tex


class Cyclo(Scene):
    level = [0, 0]

    def hide_all(self, anim: Callable[[Mobject], Animation] = FadeOut):
        if len(self.mobjects) != 0:
            self.play(
                *[anim(mob) for mob in self.mobjects]
                # All mobjects in the screen are saved in self.mobjects
            )

    def section(self):
        self.level[0] += 1
        self.level[1] = 1
        self.next_section(f"{self.level[0]}.{self.level[1]}")

    def subsection(self):
        self.hide_all()
        self.level[1] += 1

    def titlecard(self, title: str, mob: Mobject | None = None):
        text = Tex(f"{self.level[0]}.{self.level[1]} " + title)
        text.to_edge(UP + LEFT)  # pyrefly: ignore
        if mob is not None:
            self.play(FadeIn(text), FadeIn(mob))
            self.play(FadeOut(text), FadeOut(mob))
        else:
            self.play(FadeIn(text))
            self.play(FadeOut(text))
        return text

    def intro(self):

        self.section()
        self.titlecard("Something Familiar", MathTex(r"2^{2^\alpha} + 1"))
        # text = Text("Let's start with something familiar")
        # self.play(Write(text))

        fermat_full = manim.MathTex(r"p = 2^{2^\alpha} + 1")
        fermat_full.save_state()
        self.play(Write(fermat_full))

        fermat = manim.MathTex(r"p = 2^h + 1")
        self.play(Transform(fermat_full, fermat))

        down_arr = manim.MathTex(r"\Downarrow")
        down_arr.next_to(fermat, DOWN)

        fermat_examples = Text("e.g. 3, 5, 17", font_size=15)
        fermat_examples.next_to(down_arr, DOWN)
        self.play(Write(fermat_examples), FadeIn(down_arr))
        self.play(FadeOut(fermat_examples), FadeOut(down_arr))

        fermat_constraint = Tex(r"if $2^h + 1$ is prime, $h$ must be a power of 2")
        fermat_constraint.next_to(fermat, DOWN)
        self.play(Write(fermat_constraint))
        self.play(Unwrite(fermat_constraint))

        self.play(Restore(fermat_full))

        self.play(FadeOut(fermat_full))

        proof_req = Tex(r"Suppose: $h$'s largest odd factor, $w$, is greater than 1.",
                        font_size=30)
        self.play(FadeIn(proof_req))
        proof_line_1 = MathTex(r"h = 2^{\alpha}w, w > 1")
        proof_line_1.next_to(proof_req, DOWN)
        self.play(Write(proof_line_1))
        downarrow = MathTex(r"\Downarrow")
        proof_line_2 = MathTex(
            r"2^{2^{\alpha}w}+1 = \left(2^{2^{\alpha}}+1\right)\left(2^{2^{\alpha}(w-1)} - 2^{2^{\alpha}(w-2)} + ... +1\right)")

        self.play(proof_req.animate.shift(3*UP), proof_line_1.animate.shift(2*UP))

        downarrow.move_to(np.array([0,0.5,0]))
        proof_line_2.move_to(np.array([0,-0.8,0]))
        self.play(Write(downarrow), Write(proof_line_2))

        proof_line_3 = MathTex(r"2^{2^{\alpha}}+1 \mid 2^{2^{\alpha}w} + 1")
        proof_line_3.move_to(proof_line_2)
        self.play(ReplacementTransform(proof_line_2, proof_line_3))

        self.subsection()

        cyclo_ex = MathTex(r"""
            \Phi_1(x) &= x - 1 \\
            \Phi_2(x) &= x + 1 \\
            \Phi_3(x) &= x^2 + x + 1 \\
            \Phi_4(x) &= x^2 + 1 \\
            \Phi_5(x) &= x^4 + x^3 + x^2 + x + 1 \\
            \Phi_6(x) &= x^2 - x + 1\\
        """)
        self.titlecard("Something New?", cyclo_ex)

        new_fact = MathTex(r"b&\geq2,m\geq 1,h\geq 1", r"\\ p = b^{mh} + &b^{(m-1)h} + ...+ b^{h} + 1")

        new_fact.to_edge(UP)

        conc_from_fact = Tex(r"$m+1$ is prime, $h$ is a power of $m+1$")

        fact_arr = Arrow(UP, DOWN)
        fact_arr.next_to(new_fact, DOWN)
        new_fact.next_to(fact_arr, UP)
        fact_arr.next_to(conc_from_fact, UP)

        self.play(Write(new_fact))
        self.play(Write(conc_from_fact), GrowArrow(fact_arr))

        fact_highlight = SurroundingRectangle(new_fact[1], conc_from_fact, buff=.1)
        self.play(Create(fact_highlight))

        self.hide_all()

        fermat_bin = MathTex("2^{h}+1 = 1", "00...01", "_{2}")
        self.play(Write(fermat_bin))
        bin_brace = BraceLabel(fermat_bin[1], "h")
        self.play(Create(bin_brace))

        self.hide_all()

        base_b_fact = MathTex(r"\left(b^{h}\right)^{m} + \left(b^{h}\right)^{m-1} + ... + b^{h} + 1 = 1", "00...01",
                              "00..01", "...", "00...01", "_{b}")
        self.play(Write(base_b_fact))
        base_b_braces = [
            BraceLabel(base_b_fact[1], "h"),
            BraceLabel(base_b_fact[2], "h"),
            BraceLabel(base_b_fact[4], "h"),
        ]
        self.play(*[Create(x) for x in base_b_braces])

        # not sure about this one

        self.hide_all()
        stick_figure = Tex("STICK FIGURE HERE")
        self.play(FadeIn(stick_figure))
        self.wait(3.5)
        self.remove(stick_figure)

    def definition(self):
        self.section()

        defi_str = r"\Phi_n(x) = \prod_{\substack{1 \le k \le n\\gcd(k,n) = 1}} \left(x - e^{2\pi i \frac{k}{n}} \right)"

        title_defi = mt(defi_str)
                
        self.titlecard("A Definition", title_defi)

        defi = mt(defi_str)
        defi_eng = Text(
                "= the lowest degree monic polynomial whose roots are the nth primitive roots of unity",
                font_size = 20
        ).next_to(defi, DOWN)
        self.play(Write(defi))
        cursor_1 = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 0.5,
            width = 0.25,
        ).move_to(defi_eng[0]) # Position the cursor
        self.play(TypeWithCursor(defi_eng, cursor_1))
        self.play(Blink(cursor_1, blinks=2))
        self.hide_all()

        weirds = VGroup(
                tx(r"1. Primitive Roots ???"),
                tx(r"2. $\Phi$ ???"),
                tx(r"3. Integer polynomials ???"),
        ).arrange(DOWN)
        weird_highlight = SurroundingRectangle(weirds[0], buff=.1)
        weird_highlight.scale_to_fit_width(max([x.width for x in weirds]) + .2)
        self.play(FadeIn(weirds))
        self.play(FadeIn(weird_highlight))
        self.play(weird_highlight.animate.move_to(weirds[1]))
        self.play(weird_highlight.animate.move_to(weirds[2]))

    @staticmethod
    def unity(N):
        grph = VGroup()
        plane = ComplexPlane().add_coordinates()        
        grph.add(plane)

        plot = plane.plot_parametric_curve(lambda t: np.array([np.cos(t), np.sin(t)]), t_range = [0, 2*PI])
        grph.add(plot)
        points = VGroup(*[Dot(plane.n2p(np.exp(2*PI*1.j*(L / N))), color=YELLOW) for L in range(int(np.floor(N)))])
        
        grph.add(points)

        grph.add(Text(f"N = {np.around(N, 3)}", font_size=24).to_edge(UP + RIGHT)) # pyrefly: ignore
        
        return grph



    def roots_unity_sect(self):
        self.section()

        unity_6 = self.unity(6)
        
        self.titlecard("Regular Roots of Unity", unity_6)

        self.hide_all()
        stick_figure = Tex("STICK FIGURE HERE")
        self.play(FadeIn(stick_figure))
        self.wait(3.5)
        self.remove(stick_figure)

        self.hide_all()

        plane = ComplexPlane().add_coordinates()


        main_point = Dot(plane.n2p(1+0j), color=YELLOW)
        main_label = mt(r"1+0i").next_to(main_point, RIGHT)
        moving_point = Dot(plane.n2p(1+0j), color=ORANGE)

        k = ValueTracker(0)

        maths_label = mt(r"e^{2 \pi i k}", color=ORANGE).to_edge(UP + RIGHT) # pyrefly: ignore

        k_label = Text("k = 0", font_size=24)\
                .next_to(maths_label, DOWN)\
                .add_updater(
                        lambda m: m.become(Text(f"k = {np.around(k.get_value(), 3)}", font_size=24)
                                .next_to(maths_label, DOWN))
                )
        def eval_p(x) -> complex:
            return np.exp(1.j*2*PI*x)
        def cpx_str(z: complex) -> str:
            return str(np.around(z, 3)).replace("j", "i").replace(")", "").replace("(", "").replace("+", " + ").replace("-", " - ")
        
        point_label = Text("1+0i", font_size=20).add_updater(lambda m: m.become(Text(cpx_str(eval_p(k.get_value())), font_size=20)).next_to(moving_point, UP))        

        moving_point.add_updater(lambda m: m.move_arc_center_to(plane.n2p(eval_p(k.get_value()))))
        moving_point.add_updater(lambda m: m.move_arc_center_to(plane.n2p(eval_p(k.get_value()))))

        self.add(plane, main_point, moving_point, main_label, point_label, maths_label, k_label)


        self.play(ChangeSpeed(k.animate.set_value(1), speedinfo={0: 0.25}))

        self.wait()
        
        self.play(ChangeSpeed(k.animate.set_value(2), speedinfo={0: 0.25}))

        self.wait()
        
        self.play(ChangeSpeed(k.animate.set_value(3), speedinfo={0: 0.25}))


        self.hide_all()

        proof_1 = mt(r"x^n - 1 = 0")
        proof_2 = mt(r"x^n = 1")
        proof_3 = mt(r"x^n = e^{e\pi i k}")
        proof_4 = mt(r"x = e^{e\pi i \frac{k}{n}}")

        self.play(Write(proof_1))         
        self.play(ReplacementTransform(proof_1, proof_2))
        self.play(ReplacementTransform(proof_2, proof_3))
        self.play(ReplacementTransform(proof_3, proof_4))

        proof_box = SurroundingRectangle(proof_4, buff = 0.1)
        self.play(Create(proof_box))

        self.hide_all()

        N = ValueTracker(2)

        meow = self.unity(2)
        meow.add_updater(lambda m: m.become(self.unity(N.get_value())))

        self.play(FadeIn(meow))

        speed = 0.25
        self.play(ChangeSpeed(N.animate.set_value(2), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(3), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(4), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(5), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(6), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(7), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(8), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(9), speedinfo={0: speed}))
        self.play(ChangeSpeed(N.animate.set_value(10), speedinfo={0: speed}))

        self.wait()

        self.subsection()
        self.titlecard("Primitive Roots of Unity", unity_6)

        subset = tx(r"primitve roots $\subseteq$ regular roots")
        self.play(Write(subset))

        
        
        

    def phi(n: int):
        return len([k for k in range(1, n+1) if np.gcd(n, k) == 1])

    def totients(self):
        self.section()
        self.titlecard("Connections to Euler's Totient Function")
        
            
    def construct(self):
        self.intro()
        
        intro_anim = Tex("INTRO ANIM")
        self.add(intro_anim)
        self.wait(3)
        self.remove(intro_anim)

        # PLAY INTRO ANIMATION
        self.definition()

        self.roots_unity_sect()

        self.totients()

        Cyclotomics.setup(self)


