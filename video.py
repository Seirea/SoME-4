# from manim.mobject.svg.brace import BraceLabel
# from manim import VGroup
from typing import Callable
# from manim.animation.animation import Animation
# from manim.animation.creation import Create
# from manim.mobject.geometry.shape_matchers import SurroundingRectangle
# from manim.animation.growing import GrowArrow
# from manim.mobject.geometry.line import Arrow
# from manim.mobject.mobject import Mobject
# from manim.animation.transform import ReplacementTransform
# from manim.mobject.text.tex_mobject import MathTex
# from manim.animation.transform import Restore
# import manim
# from manim import Scene, Text, Tex, Write, Unwrite, FadeOut, DOWN, UP, LEFT, Transform, FadeIn
from manim import *
from rich.console import detect_legacy_windows

# print(MathTex(r"e^{2\pi i \frac{1}{6}}", r"1")[0][-1])
#
# if MathTex(r"e^{2\pi i \frac{1}{6}}", r"1")[0][7].tex_strings[0] == "6":
#     print("haha")
# else:
#     print("buh")

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

    def divisors(self, n):
        divs = []

        for i in range(1,n+1):
            if n%i == 0:
                divs.append(i)

        return divs

    def intro(self):

        self.section()
        self.subsection()
        self.titlecard("Something Familiar", MathTex(r"2^{2^\alpha} + 1"))
        # text = Text("Let's start with something familiar")
        # self.play(Write(text))

        fermat_full = MathTex(r"p = 2^{2^\alpha} + 1")
        fermat_full.save_state()
        self.play(Write(fermat_full))

        fermat = MathTex(r"p = 2^h + 1")
        self.play(Transform(fermat_full, fermat))

        down_arr = MathTex(r"\Downarrow")
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

    def definitions(self):
        self.section()
        self.subsection()
        self.titlecard("Cyclotomic Polynomials", MathTex(r"\Phi_n(x)"))


        cyclo_examples = [MathTex(r"x-1", r"=", r"(x-1)"), MathTex(r"x^2-1", r"=", r"(x-1)", r"(x+1)"), MathTex(r"x^3-1", r"=", r"(x-1)", r"(x^2+x+1)"), MathTex(r"x^4-1", r"=", r"(x-1)", r"(x+1)", r"(x^2+1)"), MathTex(r"x^5-1", r"=", r"(x-1)", r"(x^4+x^3+x^2+x+1)"), MathTex(r"x^6-1", r"=", r"(x-1)", r"(x+1)", r"(x^2+x+1)", r"(x^2-x+1)"), MathTex(r"x^7-1", r"=", r"(x-1)", r"(x^6+x^5+x^4+x^3+x^2+x+1)")]

        lhs = VGroup(cyclo_examples[i][0] for i in range(7))
        equals_signs = VGroup(cyclo_examples[i][1] for i in range(7))
        rhs = VGroup(cyclo_examples[i][2:] for i in range(7))

        lhs.arrange(DOWN, aligned_edge=RIGHT, buff=0.5)

        for l, eq, r in zip(lhs, equals_signs, rhs):
            eq.next_to(l, RIGHT, buff=0.1)
            r.next_to(eq, RIGHT, buff=0.1)

        equations = VGroup(VGroup(l, eq, r) for l, eq, r in zip(lhs, equals_signs, rhs))
        equations.move_to((0,0,0))

        self.play(Write(equations))

        arrow = MathTex(r"\rightarrow")
        arrow.next_to(cyclo_examples[0], LEFT)

        self.play(Write(arrow))

        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        finished = [[] for i in range(7)]

        for i in range(7):
            divisors = self.divisors(i+1)
            for j in range(len(divisors)):
                divisor = divisors[j]
                finished[divisor-1].append(cyclo_examples[i][j+2])
                hue = colors[divisor-1]

                if j == len(divisors)-1:
                    self.play(finished[divisor-1][-1].animate.set_color(hue))
                self.play(Indicate(finished[divisor-1][0], color = hue), Indicate(finished[divisor-1][-1], color = hue))

            if(i != 6):
                self.play(arrow.animate.next_to(cyclo_examples[i+1], LEFT))
            else:
                self.play(FadeOut(arrow))

        self.play(*[Indicate(cyclo_examples[i][0], color = WHITE) for i in range(7)])
        self.play(equations.animate.scale(0.5).move_to((0, 0, 0)))

        factorizations = [MathTex(r"{{(x-1)}}"), MathTex(r"{{(x+1)}}{{(x-1)}}"), MathTex(r"{{(x-e^{2\pi i \frac{1}{3} })(x-e^{2\pi i \frac{2}{3} })}}{{(x-1)}}"),
                          MathTex(r"{{(x-e^{2\pi i \frac{1}{4} })(x-e^{2\pi i \frac{3}{4} })}}{{(x+1)}}{{(x-1)}}"), MathTex(r"{{(x-e^{2\pi i \frac{1}{5} })(x-e^{2\pi i \frac{2}{5} })(x-e^{2\pi i \frac{3}{5} })(x-e^{2\pi i \frac{4}{5} })}}{{(x-1)}}"),
                          MathTex(r"{{(x-e^{2\pi i \frac{1}{6} })(x-e^{2\pi i \frac{5}{6} })}}{{(x-e^{2\pi i \frac{1}{3} })(x-e^{2\pi i \frac{2}{3} })}}{{(x+1)}}{{(x-1)}}"),
                          MathTex(r"{{(x-e^{2\pi i \frac{1}{7} })(x-e^{2\pi i \frac{2}{7} })(x-e^{2\pi i \frac{3}{7} })(x-e^{2\pi i \frac{4}{7} })(x-e^{2\pi i \frac{5}{7} })(x-e^{2\pi i \frac{6}{7} })}}{{(x-1)}}")]

        newLHS = VGroup(*factorizations)
        newLHS.arrange(DOWN, aligned_edge=RIGHT, buff=0.5)
        newLHS.scale(0.5)
        newLHS.move_to((-2.28, 0, 0))

        self.play(*[VGroup(equals_signs[i], rhs[i]).animate.next_to(factorizations[i], RIGHT, buff=0.1) for i in range(7)], ReplacementTransform(lhs, newLHS))

        newFinished = [[] for i in range(7)]

        arrow.next_to(factorizations[0], LEFT)
        self.play(Write(arrow))

        for i in range(7):
            divisors = self.divisors(i+1)
            for j in range(len(divisors)):
                divisor = divisors[j]
                newFinished[divisor-1].append(factorizations[i][len(divisors) - j - 1])
                hue = colors[divisor-1]

                if j == len(divisors)-1:
                    self.play(newFinished[divisor-1][-1].animate.set_color(hue))
                self.play(Indicate(newFinished[divisor-1][0], color = hue), Indicate(newFinished[divisor-1][-1], color = hue))

            if(i != 6):
                self.play(arrow.animate.next_to(factorizations[i+1][0], LEFT))
            else:
                self.play(FadeOut(arrow))

        #fading out irrelevant terms
        irrelevantTermsList = []

        for i in range(7):
            for j in range(1, len(self.divisors(i+1))):
                irrelevantTermsList.append(factorizations[i][j])

        for i in range(7):
            for j in range(len(self.divisors(i+1))):
                if j != len(self.divisors(i+1))-1:
                    irrelevantTermsList.append(cyclo_examples[i][j+2])
                else:
                    irrelevantTermsList.append(cyclo_examples[i][-1][0])
                    irrelevantTermsList.append(cyclo_examples[i][-1][-1])

        self.play(*[FadeOut(i) for i in irrelevantTermsList])

        #reordering the relevant terms (swapping LHS and RHS)

        newRHS = VGroup(factorizations[i][0] for i in range(7))
        newLHS = VGroup(cyclo_examples[i][-1][1:len(cyclo_examples[i][-1])-1] for i in range(7))
        animations = []
        eqX = -2.05

        for r, eq, l in zip(newRHS, equals_signs, newLHS):
            deltaX = eq.get_x()-eq.get_edge_center(LEFT)[0]

            animations.append(eq.animate.move_to((eqX, eq.get_y(), 0)))
            animations.append(r.animate.move_to((eqX+deltaX+0.1, eq.get_y(), 0), aligned_edge = LEFT))
            animations.append(l.animate.move_to((eqX-deltaX-0.1, eq.get_y(), 0), aligned_edge = RIGHT))

        self.play(*animations)

        #changing everything to white
        self.play(*[i.animate.set_color(WHITE) for i in newLHS], *[i.animate.set_color(WHITE) for i in newRHS])

        #highlighting denominators row-by-row
        for i in range(2,7):
            buffer = []
            for j in range(len(newRHS[i])):
                if j%11 == 9:
                    buffer.append(newRHS[i][j])

            self.play(*[Indicate(k, color = colors[i], scale_factor = 3) for k in buffer], time=2)

        #give an alternative form of lines 1 and 2
        alt1 = MathTex(r"=(x-e^{2 \pi i \frac{0}{1}})")
        alt1.scale(0.5)
        alt1.next_to(newRHS[0], direction = RIGHT, buff = 0.1)
        alt1.shift([0,newRHS[0].get_edge_center(DOWN)[1]-alt1.get_edge_center(DOWN)[1],0])

        self.play(Write(alt1))
        self.play(Indicate(alt1[0][-2], color = RED, scale_factor = 3), time = 2)

        preAlt2 = MathTex(r"=(x-(-1))")
        preAlt2.scale(0.5)
        preAlt2.next_to(newRHS[1], direction=RIGHT, buff=0.1)

        alt2 = MathTex(r"=(x-e^{2 \pi i \frac{1}{2}})")
        alt2.scale(0.5)
        alt2.next_to(newRHS[1], direction=RIGHT, buff=0.1)
        alt2.shift([0, newRHS[1].get_edge_center(DOWN)[1] - alt2.get_edge_center(DOWN)[1], 0])

        self.play(Write(preAlt2))
        self.play(ReplacementTransform(preAlt2, alt2))
        self.play(Indicate(alt2[0][-2], color = ORANGE, scale_factor = 3), time = 2)

        #writing formula for cyclotomic polynomials
        self.play(*[i.animate.shift(UP) for i in newLHS], *[i.animate.shift(UP) for i in newRHS], *[i.animate.shift(UP) for i in equals_signs], alt1.animate.shift(UP), alt2.animate.shift(UP))

        etc = MathTex(r"\vdots")
        etc.next_to(equals_signs[-1], direction = DOWN, buff = 0.5)

        self.play(Write(etc))

        newEq = MathTex(r"\Phi_n(x)", r"=", r"\prod_{\substack{0 \le k < n\\\frac{k}{n} \text{ is fully reduced} } } \left(x - e^{2\pi i \frac{k}{n} } \right)")
        newEq[1].next_to(etc, direction = DOWN, buff = 0.1)
        newEq[1].shift([0, -1, 0])
        newEq[0].next_to(newEq[1], direction = LEFT, buff = 0.1)
        newEq[2].next_to(newEq[1], direction=RIGHT, buff=0.1)

        self.play(Write(newEq))

        productAlt = MathTex(r"\substack{gcd(k,n) = 1}")
        productAlt.move_to(newEq[2][6:23])

        self.play(Transform(newEq[2][6:23], productAlt))

        eqBox = SurroundingRectangle(newEq, buff = 0.1)
        self.play(Create(eqBox))

        self.wait(4)

    def construct(self):
        # play intro animation
        self.intro()
        # play definitions animation
        self.definitions()