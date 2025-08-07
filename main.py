from manim.mobject.types.vectorized_mobject import VGroup
from cloup.formatting._formatter import Definition
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
from manim import Scene, Text, Tex, Write, Unwrite, FadeOut, DOWN, UP, LEFT, Transform, FadeIn
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
        self.level[1] = 0
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
        self.subsection()
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
        self.subsection()

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
        
    
    def construct(self):
        self.intro()
        
        intro_anim = Tex("INTRO ANIM")
        self.add(intro_anim)
        self.wait(3)
        self.remove(intro_anim)

        self.definition()
        # PLAY INTRO ANIMATION
