from manim.mobject.svg.brace import BraceLabel
from manim import VGroup
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
from rich.console import detect_legacy_windows


# class SectionDisplay(Tex):


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
        proof_line_2 = MathTex(r"2^{2^\alpha}+1\equiv 0 \mod{2^{2^\alpha}+1}")

        self.play(proof_req.animate.shift(3*UP), proof_line_1.animate.shift(2*UP))

        downarrow.move_to([0,0.5,0])
        proof_line_2.move_to([0,-0.8,0])
        self.play(Write(downarrow), Write(proof_line_2))
        proof_line_3 = MathTex(r"2^{2^\alpha}\equiv -1 \mod{2^{2^\alpha}+1}")
        proof_line_3.move_to(proof_line_2)
        proof_line_4 = MathTex(r"2^{2^\alpha w}\equiv (-1)^w \mod{2^{2^\alpha}+1}")
        proof_line_4.move_to(proof_line_2)
        proof_line_5 = MathTex(r"2^{2^\alpha w}\equiv -1 \mod{2^{2^\alpha}+1}")
        proof_line_5.move_to(proof_line_2)
        proof_line_6 = MathTex(r"2^{2^\alpha w}+1 \equiv 0 \mod{2^{2^\alpha}+1}")
        proof_line_6.move_to(proof_line_2)
        proof_line_7 = MathTex(r"2^{2^{\alpha}}+1 \mid 2^{2^{\alpha}w} + 1, 2^{2^{\alpha}}+1 \neq 1, 2^{2^{\alpha}}+1 \neq 2^{2^{\alpha}w}+1")
        proof_line_7.move_to(proof_line_2)
        self.play(ReplacementTransform(proof_line_2, proof_line_3))
        self.play(ReplacementTransform(proof_line_3, proof_line_4))
        self.play(ReplacementTransform(proof_line_4, proof_line_5))
        self.play(ReplacementTransform(proof_line_5, proof_line_6))
        self.play(ReplacementTransform(proof_line_6, proof_line_7))

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
        stick_figure = Tex("STICK FIGURE")  # i can make one for us :)
        self.play(Create(stick_figure))
        self.play(FadeOut(stick_figure))

        cyclotomic_examples = MathTex(r"\Phi_1(x) &= x - 1 \\ \Phi_2(x) &= x + 1 \\ \Phi_3(x) &= x^2 + x + 1 \\ \Phi_4(x) &= x^2 + 1 \\ "
                                      r"\Phi_5(x) &= x^4 + x^3 + x^2 + x + 1 \\ \Phi_6(x) &= x^2 - x + 1 \\ \Phi_7(x) &= x^6 + x^5 + x^4 + x^3 + x^2 + x + 1 \\ \Phi_8(x) &= x^4 + 1 \\"
                                      r"\Phi_9(x) &= x^6 + x^3 + 1 \\ \Phi_{10}(x) &= x^4 - x^3 + x^2 - x + 1")
        self.play(Write(cyclotomic_examples))

    def divisors(self, n):
        divs = []

        for i in range(1,n+1):
            if n%i == 0:
                divs.append(i)

        return divs

    def definitions(self):
        self.section()
        self.subsection()
        self.titlecard("Cyclotomic Polynomials", MathTex(r"\Phi_n(x)"))

        cyclo_examples = MathTex(r"{{x-1&=}} {{(x-1)}} \\", r"{{x^2-1&=}} {{(x-1)}} {{(x+1)}} \\", r"{{x^3-1&=}} {{(x-1)}} {{(x^2+x+1)}} \\", r"{{x^4-1&=}} {{(x-1)}} {{(x+1)}} {{(x^2+1)}} \\", r"{{x^5-1&=}} {{(x-1)}} {{(x^4+x^3+x^2+x+1)}} \\", r"{{x^6-1&=}} {{(x-1)}} {{(x+1)}} {{(x^2+x+1)}} {{(x^2-x+1)}} \\", r"{{x^7-1&=}} {{(x-1)}} {{(x^6+x^5+x^4+x^3+x^2+x+1)}}")
        cyclo_examples.move_to([0,0,0])
        self.play(Write(cyclo_examples))

        colors = [manim.RED, manim.ORANGE, manim.YELLOW, manim.GREEN, manim.BLUE, manim.PURPLE, manim.PINK]
        finished = [[] for i in range(7)]

        for i in range(7):
            divisors = self.divisors(i+1)
            for j in range(len(divisors)):
                divisor = divisors[j]
                finished[divisor-1].append(cyclo_examples[i])
                hue = colors[divisor-1]

                fact_highlight = SurroundingRectangle(finished[divisor-1][-1], color = hue, buff = .1)
                self.play(Create(fact_highlight), *[manim.Indicate(k, color = hue) for k in finished[divisor-1]])

    def construct(self):
        #self.intro()
        self.definitions()
        # PLAY INTRO ANIMATION