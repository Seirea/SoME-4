from manim.mobject.geometry.line import Line
from manim.animation.speedmodifier import ChangeSpeed
from manim.constants import PI
from manim.mobject.value_tracker import ValueTracker
from manim.mobject.geometry.arc import Dot
from manim.mobject.types.point_cloud_mobject import Point
from manim.mobject.graphing.coordinate_systems import ComplexPlane
from manim.utils.color.manim_colors import WHITE, BLACK
from manim.animation.indication import Indicate
from manim.utils.color.manim_colors import PINK
from manim.utils.color.manim_colors import PURPLE
from manim.utils.color.manim_colors import BLUE
from manim.utils.color.manim_colors import GREEN
from manim.utils.color.manim_colors import YELLOW
from manim.utils.color.manim_colors import ORANGE
from manim.utils.color.manim_colors import RED
from manim.mobject.svg.brace import BraceLabel
from manim import VGroup, Rectangle
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
# import manim
from manim import Scene, Text, Tex, Write, Unwrite, FadeOut, DOWN, UP, LEFT, RIGHT, Transform, FadeIn
# from manim import *
# from rich.console import detect_legacy_windows
import numpy as np
from manim import AnimationGroup

mt = MathTex
pre_angle = 0

# print(MathTex(r"e^{2\pi i \frac{1}{6}}", r"1")[0][-1])
#
# if MathTex(r"e^{2\pi i \frac{1}{6}}", r"1")[0][7].tex_strings[0] == "6":
#     print("haha")
# else:
#     print("buh")

class Cyclo(Scene):
    level = [0, 0, 0]

    def hide_all(self, anim: Callable[[Mobject], Animation] = FadeOut):
        if self.mobjects is not None and len(self.mobjects) != 0:
            self.play(
                *[anim(mob) for mob in self.mobjects]
                # All mobjects in the screen are saved in self.mobjects
            )

    def section(self):
        self.level[0] += 1
        self.level[1] = 0
        self.level[2] = 0

    def subsection(self):
        self.hide_all()
        self.level[1] += 1

    def subsubsection(self):
        self.hide_all()
        self.level[2] += 1

    def titlecard(self, title: str, mob: Mobject | None = None):
        subt = (
            "" if self.level[1] == 0 and self.level[2] == 0
            else f".{self.level[1]}" if self.level[2] == 0
            else f".{self.level[1]}.{self.level[2]}")

        text = Tex(f"{self.level[0]}{subt} " + title)
        text.to_edge(UP + LEFT)  # pyrefly: ignore
        if mob is not None:
            self.play(FadeIn(text), FadeIn(mob))
            self.play(FadeOut(text), FadeOut(mob))
        else:
            if self.level[1] == 0:
                text.move_to(np.array((0, 0, 0)))
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

        self.next_section("1", skip_animations = True)

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
                self.play(Indicate(finished[divisor-1][0], color = str(hue)), Indicate(finished[divisor-1][-1], color = str(hue)))

            if(i != 6):
                self.play(arrow.animate.next_to(cyclo_examples[i+1], LEFT))
            else:
                self.play(FadeOut(arrow))

        self.play(*[Indicate(cyclo_examples[i][0], color = str(WHITE)) for i in range(7)])
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
                self.play(Indicate(newFinished[divisor-1][0], color = str(hue)), Indicate(newFinished[divisor-1][-1], color = str(hue)))

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
        newEq[1].shift(np.array([0, -1, 0]))
        newEq[0].next_to(newEq[1], direction = LEFT, buff = 0.1)
        newEq[2].next_to(newEq[1], direction=RIGHT, buff=0.1)

        self.play(Write(newEq))

        productAlt = MathTex(r"\substack{gcd(k,n) = 1}")
        productAlt.move_to(newEq[2][6:23])

        self.play(Transform(newEq[2][6:23], productAlt))

        eqBox = SurroundingRectangle(newEq, buff = 0.1)
        self.play(Create(eqBox))

        self.next_section("2", skip_animations = False)
        #primes section

        self.subsection()
        self.titlecard("For Primes", mt(r"x^{q-1}+x^{q-2}+...+x+1"))

        cyclo_examples_p = [mt(r"\Phi_1(x)", "=", "x - 1"), mt(r"\Phi_2(x)", "=", "x + 1"), mt(r"\Phi_3(x)", "=", r"x^2 + x + 1"), mt(r"\Phi_4(x)", "=", r"x^2 + 1"),
            mt(r"\Phi_5(x)", "=", r"x^4 + x^3 + x^2 + x + 1"), mt(r"\Phi_6(x)", "=", r"x^2 - x + 1"), mt(r"\Phi_7(x)", "=", r"x^6 + x^5 + x^4 + x^3 + x^2 + x + 1")]

        lhs = VGroup(cyclo_examples_p[i][0] for i in range(7))
        equals_signs = VGroup(cyclo_examples_p[i][1] for i in range(7))
        rhs = VGroup(cyclo_examples_p[i][2:] for i in range(7))

        lhs.arrange(DOWN, aligned_edge=RIGHT, buff=0.5)

        for l, eq, r in zip(lhs, equals_signs, rhs):
            eq.next_to(l, RIGHT, buff=0.1)
            r.next_to(eq, RIGHT, buff=0.1)

        equations = VGroup(VGroup(l, eq, r) for l, eq, r in zip(lhs, equals_signs, rhs))
        equations.move_to((0, 0, 0))

        self.play(Write(equations))

        primeRows = VGroup(*[cyclo_examples_p[i-1] for i in [2,3,5,7]])
        nonPrimeRows = VGroup(*[cyclo_examples_p[i-1] for i in [1,4,6]])
        self.play(FadeOut(nonPrimeRows), primeRows.animate.arrange(DOWN, aligned_edge = LEFT))

        animGroupList = []

        for i in range(7):
            buffer = []
            for j in range(4):
                maxIndex = 3*([2,3,5,7][j]-2)+2
                if 3*i+3 <= maxIndex:
                    buffer.append(primeRows[j][2][3*i:3*i+2])
                elif 3*i < maxIndex:
                    buffer.append(primeRows[j][2][3*i])
                elif 3*i-3 < maxIndex:
                    buffer.append(primeRows[j][2][maxIndex])

            animGroupList.append(Indicate(VGroup(*buffer)).set_run_time(0.5))

        animGroup = AnimationGroup(*animGroupList, lag_ratio = 0.2)
        self.play(animGroup)


            # self.play(*[Indicate(primeRows[j][2][i]) for j in range(4) if [2,3,5,7][j] >= i], time = 0.65)

        newLHS = mt(r"\Phi_p(x)")
        newRHS = mt(r"x^{p-1}+x^{p-2}+...+x+1")
        eq = mt("=")
        qmark = mt("?")
        eq.move_to(equals_signs)
        newLHS.next_to(eq, direction = LEFT)
        newRHS.next_to(eq, direction = RIGHT)
        qmark.next_to(newRHS, direction = RIGHT)
        equation = VGroup(newLHS, eq, newRHS)

        self.play(ReplacementTransform(primeRows, equation))
        self.play(Write(qmark))
        equation = VGroup(newLHS, eq, newRHS)
        self.play(FadeOut(qmark))
        self.play(Indicate(equation, color = WHITE))

        geo_form = mt(r"\frac{x^p-1}{x-1}")
        geo_form.next_to(equation[1], direction = RIGHT)
        self.play(Transform(equation[2], geo_form))
        self.play(equation.animate.shift([-equation[1].get_x(), -equation[1].get_y(), -equation[1].get_z()]))

        phi_p = mt(r"\prod_{\substack{0 \le k \le p\\gcd(k,p) = 1}} \left(x - e^{2\pi i \frac{k}{p}} \right)")
        phi_p.next_to(equation[1], direction = LEFT)
        self.play(Transform(equation[0], phi_p))

        newSubstack = mt(r"\substack{p\nmid k}")
        newSubstack1 = mt(r"\substack{k \neq 0}")

        newSubstack.move_to(equation[0][0][6:16])
        newSubstack1.move_to(equation[0][0][6:16])

        self.play(equation[0][0][6:16].animate.become(newSubstack))
        self.play(equation[0][0][6:16].animate.become(newSubstack1))
        self.play(FadeOut(equation[0][0][6:16]))
        one = mt(r"\substack{1}")
        one.move_to(equation[0][0][1])
        self.play(equation[0][0][1].animate.become(one))

        # #index 4
        # bufferRHS = mt(r"\frac{\prod_{\substack{0 \le k \le p}} \left(x - e^{2\pi i \frac{k}{p}} \right)}{x-1}")
        #

        self.next_section("3", skip_animations=False)

        newFraction = mt(r"\frac{\prod_{\substack{0 \le k \le p}} \left(x - e^{2\pi i \frac{k}{p}} \right)}{x-1}")
        newFraction.next_to(equation[1], direction = RIGHT)
        self.play(ReplacementTransform(equation[2][0][4], newFraction[0][17]), ReplacementTransform(equation[2][0][:4], newFraction[0][:17]), ReplacementTransform(equation[2][0][5:], newFraction[0][18:]))

        exponentialForm = mt(r"e^0")
        exponentialForm.next_to(newFraction[0][19], direction = RIGHT)
        self.play(Transform(newFraction[0][20], exponentialForm))

        exponentialForm = mt(r"e^{2\pi i \frac{0}{p}}")
        exponentialForm.next_to(newFraction[0][19], direction=RIGHT)
        self.play(Transform(newFraction[0][20], exponentialForm))

        one.move_to(newFraction[0][1])
        self.play(FadeOut(newFraction[0][17:]), Transform(newFraction[0][1], one))
        # equationTransform("r", r"\frac{\prod_{\substack{0 \le k \le p}} \left(x - e^{2\pi i \frac{k}{p}} \right)}{x-e^0}")
        # equationTransform("r", r"\frac{\prod_{\substack{0 \le k \le p}} \left(x - e^{2\pi i \frac{k}{p}} \right)}{x-e^{2\pi i \frac{0}{p}}}")
        # equationTransform("r", r"\prod_{\substack{1 \le k \le p}} \left(x - e^{2\pi i \frac{k}{p}} \right)")

        newRHS = phi_p.copy()
        newRHS.next_to(eq, direction = RIGHT)
        newRHS.shift([0, phi_p.get_y()-newRHS.get_y(), 0])

        self.play(newFraction[0][0].animate.scale_to_fit_height(newRHS[0][0].height).move_to(newRHS[0][0]), newFraction[0][1:6].animate.move_to(newRHS[0][1:6]), newFraction[0][6:17].animate.move_to(newRHS[0][16:27]))

        self.play(Indicate(newFraction[0][:17]), Indicate(equation[0][0][:6]), Indicate(equation[0][0][16:]))

        self.wait(4)

    def the_result(self):
        self.next_section("result 1", skip_animations=False)

        self.section()
        self.titlecard("The Central Result")
        # ...

        self.subsection()
        self.titlecard("Divisibility", mt(r"\Phi_{hq}(x)\mid\Phi_q(x^h)"))

        prod = mt(r"\Phi_n(x)=\prod_{\substack{0\leq k \leq n \\ \gcd(k,n) = 1}}\left(x-e^{2\pi i \frac{k}{n}}\right)")
        prod2 = mt(r"\Phi_{hq}(x)=\prod_{\substack{0\leq k \leq hq \\ \gcd(k,hq) = 1}}\left(x-e^{2\pi i \frac{k}{hq}}\right)")

        self.play(Write(prod))
        self.play(prod.animate.become(prod2))
        self.play(prod.animate.to_edge(UP))

        # self.play(Transform(prod, prod2))
        lrarrow = mt(r"\leftrightarrow").move_to(np.array([0,0,0]))
        divis = mt(r"\Phi_{hq}(x)\mid\Phi_q(x^h)").next_to(lrarrow, LEFT)
        multi = VGroup(
                mt(r"(x-e^{2\pi i \frac{1}{hq}})\mid \Phi_q(x^h)"),
                mt(r"\vdots"),
                mt(r"(x-e^{2\pi i \frac{hq-1}{hq}})\mid \Phi_q(x^h)"),
        ).arrange(DOWN).next_to(lrarrow, RIGHT)

        self.play(FadeIn(lrarrow), Write(divis))
        self.play(Write(multi))

        new_multi = VGroup(
                mt(r"&\forall \ 0\leq k \leq hq \text{ where}\\ &\gcd(k,hq)=1\text{:}", font_size=30),
                mt(r"(x-e^{2\pi i \frac{k}{hq}})\mid \Phi_q(x^h)")
        ).arrange(DOWN).move_to(multi)

        self.play(multi.animate.become(new_multi))

        new_multi = VGroup(
                mt(r"&\forall \ 0\leq k \leq hq \text{ where}\\ &\gcd(k,hq)=1\text{:}", font_size=30),
                mt(r"\Phi_q(x^h)\mid_{e^{2\pi i \frac{k}{hq}}} = 0")
        ).arrange(DOWN).move_to(multi)

        self.play(multi.animate.become(new_multi))

        new_multi = VGroup(
                mt(r"&\forall \ 0\leq k \leq hq \text{ where}\\ &\gcd(k,hq)=1\text{:}", font_size=30),
                mt(r"\Phi_q\left(\left(e^{2\pi i \frac{k}{hq}}\right)^h\right) = 0")
        ).arrange(DOWN).move_to(multi)
   
        self.play(multi.animate.become(new_multi))

        new_multi = VGroup(
                mt(r"&\forall \ 0\leq k \leq hq \text{ where}\\ &\gcd(k,hq)=1\text{:}", font_size=30),
                mt(r"\Phi_q\left(e^{2\pi i \frac{k}{q}}\right) = 0")
        ).arrange(DOWN).move_to(multi)
              
        self.play(multi.animate.become(new_multi))

        new_multi = VGroup(
                mt(r"&\forall \ 0\leq k \leq hq \text{ where}\\ &", r"\gcd(k,h)=1", r"\text{ and } \gcd(k, q)=1\text{:}", font_size=30),
                mt(r"\Phi_q\left(e^{2\pi i \frac{k}{q}}\right) = 0")
        ).arrange(DOWN).move_to(multi)
      
        self.play(multi.animate.become(new_multi))

        self.play(Indicate(multi[0][1]))

        zeq = mt(r"0 = 0")

        new_multi = VGroup(
                mt(r"&\forall \ 0\leq k \leq hq \text{ where}\\ &", r"\gcd(k,h)=1", r"\text{ and } \gcd(k, q)=1\text{:}", font_size=28),
                zeq
        ).arrange(DOWN).move_to(multi)
      
        self.play(multi.animate.become(new_multi))

        zeq1 = mt(r"0 = 0")

        new_multi = VGroup(
                mt(r"&\forall \ 0\leq k \leq hq \text{ where}\\ &", r"\gcd(k,h)=1", r"\text{ and } \gcd(k, q)=1\text{:}", font_size=28),
                zeq1.set_opacity(0)
        ).arrange(DOWN).move_to(multi)
      
        multi.become(new_multi)
        
        self.play(Indicate(zeq))

        self.play(FadeOut(lrarrow), FadeOut(multi), divis.animate.move_to(np.array((0,0,0))), FadeOut(zeq))

        Q_mult = mt(r"Q(x)\cdot\Phi_{hq}(x)=\Phi_q(x^h)")
        where_q = mt(r"\text{where } Q(x)=\prod_{\substack{\text{for some} \\ \text{k where} \\ 1 \leq k \leq hq }} \left(x-e^{2\pi i \frac{k}{hq} }\right) ").next_to(Q_mult, DOWN)
        arrow = mt(r"\nearrow").next_to(where_q, DOWN)
        might_be = Tex(r"might be empty")
        arrow.shift([where_q[0][9].get_x()-arrow[0][0].get_x(), 0, 0])
        might_be.next_to(arrow, LEFT)
        might_be.shift(DOWN*0.5)

        self.play(Transform(divis, Q_mult), Write(where_q), Write(arrow), Write(might_be))
        
        highBox = SurroundingRectangle(divis, buff = 0.1)
        self.play(Create(highBox))

        self.next_section("result 2", skip_animations=False)
        self.subsection()
        self.subsection()
        self.titlecard("Complex Magnitudes", mt(r"\|a+bi\|=\sqrt{a^2+b^2}"))

        monic_polys = mt(r"Q(x)", r"\cdot", r"\Phi_{hq}(x)", "=", r"\Phi_q(x^h)")
        arrows = mt(r"\nwarrow\ &\ \ \ \nearrow").next_to(monic_polys, DOWN)
        arrows.shift(np.array((monic_polys[3].get_x() - arrows.get_x(), 0, 0)))
        label = Tex(r"monic integer polynomials").next_to(arrows, DOWN)

        self.play(Write(monic_polys))
        self.wait()
        self.play(Write(arrows), FadeIn(label))
        self.play(Indicate(monic_polys[2]),Indicate(monic_polys[-1]))
        self.play(Indicate(monic_polys[0]))
        self.play(FadeOut(arrows), FadeOut(label))

        new_exp = mt(r"Q(b)", r"\cdot", r"\Phi_{hq}(b)", "=", r"\Phi_q(b^h)")

        self.play(ReplacementTransform(monic_polys[0][:2], new_exp[0][:2]),
                  ReplacementTransform(monic_polys[0][2], new_exp[0][2]),
                  ReplacementTransform(monic_polys[0][3], new_exp[0][3]),
                  ReplacementTransform(monic_polys[1], new_exp[1]),
                  ReplacementTransform(monic_polys[2][:4], new_exp[2][:4]),
                  ReplacementTransform(monic_polys[2][4], new_exp[2][4]),
                  ReplacementTransform(monic_polys[2][5], new_exp[2][5]),
                  ReplacementTransform(monic_polys[3:], new_exp[3:]))

        eq_b = mt("= p")
        eq_b.next_to(monic_polys, RIGHT)
        eq_b.shift([0, monic_polys[3].get_y()-eq_b[0][0].get_y(), 0])
        self.play(Write(eq_b))
        self.play(FadeOut(new_exp[-1]), FadeOut(new_exp[-2]), eq_b.animate.shift([monic_polys[3].get_x()-eq_b[0][0].get_x(), 0, 0]))

        monic_polys_b1 = mt(r"|Q(b)|", r"\cdot", r"|\Phi_{hq}(b)|")
        monic_polys_b1.next_to(eq_b[0][0], direction = LEFT)

        self.play(new_exp[0].animate.move_to(monic_polys_b1[0]), new_exp[1].animate.move_to(monic_polys_b1[1]), new_exp[2].animate.move_to(monic_polys_b1[2]))
        self.play(Write(monic_polys_b1[i][j]) for i,j in zip([0,2,2,0], [0,-1,0,-1]))

        eq1 = mt(r"|\Phi_{hq}(b)|", "=", "1")
        orz = Tex("or")
        eq2 = mt(r"|Q(b)|", "=", "1")

        eq1.next_to(monic_polys[1], DOWN)
        eq1.shift(DOWN)
        orz.next_to(eq1, DOWN)
        eq2.next_to(orz, DOWN)
        eq2.shift([eq1[1].get_x()-eq2[1].get_x(), 0, 0])

        self.play(AnimationGroup(Write(eq1), Write(orz), Write(eq2), lag_ratio = 0.2))

        new_eq = VGroup(monic_polys_b1[0][0], monic_polys_b1[0][-1], monic_polys_b1[2][0], monic_polys_b1[2][-1], new_exp[0:3], eq_b)
        self.play(FadeOut(orz), new_eq.animate.to_edge(UP))

        self.play(eq1.animate.shift(3*UP), eq2.animate.shift(UP))

        mag_phi_hq = mt(r"|\Phi_{hq}(b)|", "=", r"\Big\|", r"\prod_{\substack{1 \leq k \leq hq \\ \gcd(k, hq)=1} }", r"(b-e^{2\pi i \frac{k}{hq} })", r"\Big\|")
        mag_phi_hq2 = mt(r"|\Phi_{hq}(b)|", "=", r"\prod_{\substack{1 \leq k \leq hq \\ \gcd(k, hq)=1} }", r"\Big\|", r"b-e^{2\pi i \frac{k}{hq} }", r"\Big\|")
        mag_phi_hq.shift(np.array(eq1[1].get_center().tolist())-np.array(mag_phi_hq[1].get_center().tolist()))
        mag_phi_hq2.shift(np.array(eq1[1].get_center().tolist())-np.array(mag_phi_hq2[1].get_center().tolist()))

        mag_q  = mt(r"|Q(b)|", "=", r"\Big\|", r"\prod_{\substack{\text{for some} \\ \text{k where} \\ 1 \leq k \leq hq } }", r"(b-e^{2\pi i \frac{k}{hq} })", r"\Big\|").next_to(mag_phi_hq, DOWN)
        mag_q2 = mt(r"\left|Q(b)\right|", "=", r"\prod_{\substack{\text{for some} \\ \text{k where} \\ 1 \leq k \leq hq } }", r"\Big\|", r"b-e^{2\pi i \frac{k}{hq} }", r"\Big\|").next_to(mag_phi_hq, DOWN)
        mag_q.shift(np.array(eq2[1].get_center().tolist()) - np.array(mag_q[1].get_center().tolist()))
        mag_q2.shift(np.array(eq2[1].get_center().tolist()) - np.array(mag_q2[1].get_center().tolist()))

        self.play(ReplacementTransform(eq1[:2], mag_phi_hq[:2]),
                  ReplacementTransform(eq2[:2], mag_q[:2]),
                  ReplacementTransform(eq1[2], mag_phi_hq[2:]),
                  ReplacementTransform(eq2[2], mag_q[2:]))

        def rearrange(a, b):
            return a.animate.scale_to_fit_height(b.height).move_to(b)

        self.play(ReplacementTransform(mag_phi_hq[:2], mag_phi_hq2[:2]),
                  ReplacementTransform(mag_q[:2], mag_q2[:2]),
                  rearrange(mag_phi_hq[2], mag_phi_hq2[3]),
                  rearrange(mag_q[2], mag_q2[3]),
                  rearrange(mag_phi_hq[3], mag_phi_hq2[2]),
                  rearrange(mag_q[3], mag_q2[2]),
                  rearrange(mag_phi_hq[4][1:-1], mag_phi_hq2[4]),
                  rearrange(mag_q[4][1:-1], mag_q2[4]),
                  rearrange(mag_phi_hq[5], mag_phi_hq2[5]),
                  rearrange(mag_q[5], mag_q2[5]),
                  FadeOut(mag_phi_hq[4][0]),
                  FadeOut(mag_phi_hq[4][-1]),
                  FadeOut(mag_q[4][0]),
                  FadeOut(mag_q[4][-1]))

        mag1 = VGroup(mag_phi_hq[2], mag_phi_hq[4][1:-1], mag_phi_hq[5])
        mag2 = VGroup(mag_q[2], mag_q[4][1:-1], mag_q[5])

        self.play(Indicate(mag1), Indicate(mag2))

        #self.play(Write(mag_phi_hq), Write(mag_q))
        #self.play(ReplacementTransform(mag_phi_hq, mag_phi_hq_2), ReplacementTransform(mag_q, mag_q2))

        #surr1 = SurroundingRectangle(mag_phi_hq[1], buff=0.2)
        #surr2 = SurroundingRectangle(mag_q[1], buff=0.2)

        #self.play(Create(surr1), Create(surr2))
        #self.play(FadeOut(surr1), FadeOut(surr2))

        self.wait()

        self.next_section("result 3", skip_animations=False) #TODO REMOVE LATER

        self.subsubsection()
        self.titlecard("", mt(r"\left\|b-e^{2\pi i\frac{k}{hq}}\right\|"))



        plane = ComplexPlane(
            #x_range=[-4, 4],
            #y_range=[2, -1],
            background_line_style={"stroke_opacity": 0},
        ).add_coordinates(
            -4, -3, -2, -2, 1.j, -1.j, 1, 2, 3, 4
        ).scale(5/3).shift([0,1.1,0])

        y_axis = plane.get_axes()[1]
        new_y_axis = Line(
            start=plane.c2p(0, -1.2),
            end=plane.c2p(0, plane.y_range[1]),
            stroke_width=y_axis.stroke_width
        )
        plane.remove(y_axis)
        plane.add(new_y_axis)

        # mask = Rectangle(
        #     color=BLACK, fill_color=BLACK, fill_opacity=1,
        #     width=4,  # just wide enough to cover the axis
        #     height=2,
        #     z_index=100,
        # ).move_to(plane.n2p(-2.j))

        moving_point = Dot(plane.n2p(1+0j), color=ORANGE)

        k = ValueTracker(PI/4)

        #maths_label = mt(r"e^{i \theta}", color=ORANGE).to_edge(UP + RIGHT) # pyrefly: ignore
        b_label = mt("b", font_size = 35, color = ORANGE).move_to(plane.n2p(2)).shift([0, 0.3, 0])
        b_point = Dot(plane.n2p(2), color = ORANGE)

        #k_label = Text("θ = 0", font_size=24)\
                # .next_to(maths_label, DOWN)\
                # .add_updater(
                #         lambda m: m.become(Text(f"θ = {np.around(k.get_value(), 3)}", font_size=24)
                #                 .next_to(maths_label, DOWN))
                # )
                
        def eval_p(x) -> complex:
            return np.exp(1.j*x)
        def eval_rot(theta) -> float:
                # global pre_angle
                
                return -np.arctan(np.sin(theta)/(2-np.cos(theta)))
                # dtheta = pre_angle - new_angle
                # pre_angle = new_angle
                # return dtheta
        def cpx_str(z: complex) -> str:
            return str(np.around(z, 3)).replace("j", "i").replace(")", "").replace("(", "").replace("+", " + ").replace("-", " - ")


        origin_b_line = Line(plane.n2p(0), plane.n2p(2), color = GREEN)

        inner_radius = Line(np.array((0,0,0)), np.array((0,0,0)), stroke_width = 1.5)
        inner_radius.add_updater(lambda m: m.become(Line(
                plane.n2p(0),
                plane.n2p(eval_p(k.get_value())),
                stroke_width = 1.5,
                color = PINK
        )))
        
        outer_line = Line(np.array((0,0,0)), np.array((0,0,0)), stroke_width = 1.5)
        outer_line.add_updater(lambda m: m.become(Line(
                plane.n2p(eval_p(k.get_value())),
                plane.n2p(2), 0,
                stroke_width = 1.5,
                color = PINK
        )))

        value_label = mt(r"e^{i\theta}", font_size = 35, color = ORANGE).next_to(moving_point, UP, buff = 0.1).add_updater(
            lambda m: m.become (mt(rf"e^{{i {np.around(k.get_value(), 2)} }}", font_size = 35, color = ORANGE).next_to(moving_point, UP, buff = 0.1))
        )


        length_label = mt(r"\left\|b-e^{i \theta}\right\|", font_size = 30, color = ORANGE)
        length_label.add_updater(
                lambda m: m
                        .become(mt(rf"\left\|b-e^{{i {np.around(k.get_value(), 2)} }}\right\|", font_size = 30, color = ORANGE))
                        .move_to(plane.n2p((eval_p(k.get_value())+2)/2))
                        .shift( np.array([ 0, 0.2, 0 ]) )
                        .rotate( eval_rot( k.get_value() ))
        )


        circle = plane.plot_parametric_curve(lambda t: np.array([np.cos(t), np.sin(t)]), t_range = [0, 2*PI], stroke_width = 1)

        moving_point.add_updater(lambda m: m.move_arc_center_to(plane.n2p(eval_p(k.get_value()))))
        moving_point.add_updater(lambda m: m.move_arc_center_to(plane.n2p(eval_p(k.get_value()))))

        self.play(Create(plane), Create(circle))
        self.play(Create(moving_point))
        self.play(Write(value_label))
        self.play(Write(b_label), Create(b_point))
        self.play(Create(inner_radius), Create(outer_line))
        self.play(Write(length_label))

        self.play(Indicate(origin_b_line))

        self.play(outer_line.animate.set_color(PINK), Indicate(outer_line), inner_radius.animate.set_color(PINK), Indicate(inner_radius))

        bottom_magni = mt(r"1", r"+", r"\left\|b-e^{i\theta}\right\|\geq b").to_edge(DOWN)
        self.play(Write(bottom_magni))

        self.play(ChangeSpeed(k.animate.set_value(2*PI), speedinfo={0: 0.125}))

        theta_thing = mt(r"\theta = 2\pi\frac{k}{hq} \neq 0").next_to(bottom_magni, UP)

        self.play(Write(theta_thing))

        bottom_magni2 = mt(r"1+\left\|b-e^{i\theta}\right\| > b").to_edge(DOWN)
        self.play(Unwrite(theta_thing), Transform(bottom_magni[2][-2], bottom_magni2[0][-2]))

        self.play(ChangeSpeed(k.animate.set_value(2*PI+PI/4), speedinfo={0: 1}))

        bottom_magni3 = mt(r"\left\|b-e^{i\theta}\right\| > b - 1")
        bottom_magni3.shift(np.array(bottom_magni[2][-2].get_center().tolist())-np.array(bottom_magni3[0][-4].get_center().tolist()))

        self.play(rearrange(bottom_magni[1], bottom_magni3[0][-2]), rearrange(bottom_magni[0], bottom_magni3[0][-1]), Transform(bottom_magni[1], bottom_magni3[0][-2]))

        rightmost = mt(r"\geq", "2 - 1")
        rightmost.next_to(bottom_magni[0], RIGHT)

        self.play(Write(rightmost))

        one = mt(r"1")
        one.next_to(rightmost[0], RIGHT)
        self.play(ReplacementTransform(rightmost[1], one))

        letGo = VGroup(bottom_magni[0], bottom_magni[1], bottom_magni[2][-1], rightmost[0])
        self.play(FadeOut(letGo), one.animate.next_to(bottom_magni[2][-2], RIGHT))

        surr_magni = SurroundingRectangle(bottom_magni[2][:-1], one, buff=0.1)
        self.play(Create(surr_magni))
        self.play(FadeOut(surr_magni))

        #self.play(outer_line.animate.set_opacity(0), inner_radius.animate.set_opacity(0), value_label.animate.set_opacity(0), length_label.animate.set_opacity(0))
        inner_radius.remove_updater(inner_radius.updaters[0])
        outer_line.remove_updater(outer_line.updaters[0])
        value_label.remove_updater(value_label.updaters[0])
        length_label.remove_updater(length_label.updaters[0])

        self.hide_all()

    def step_27(self):
        # Step 27
        self.hide_all()

        a27 = mt(r"|Q(b)|", r"\times", r"|\Phi_{hq}(b)| = p").shift(UP)
        a27.to_edge(UP)
        b27 = mt(r"\prod_{\substack{1 \leq k \leq hq \\ \gcd(k, hq) = 1}} || b-e^{i2\pi \frac{k}{hq}} || = |\Phi_{hq} (b)|")
        b27.next_to(a27, DOWN)
        b27.shift(DOWN)
        c27 = mt(r"\prod_{\substack{\text{for some} \\ \text{k where} \\ 1 \leq k \leq hq}} || b-e^{i2\pi \frac{k}{hq}} || = |Q(b)|")

        c27.next_to(b27, DOWN)
        c27.shift(DOWN)

        self.play(Write(a27), Write(b27), Write(c27))
        self.wait()
        # Step 28

        d27 = mt(r"1 <")
        d27.next_to(b27, LEFT)
        self.play(Write(d27))

        self.wait()

        # Step 29
        self.play(FadeOut(c27), FadeOut(d27))
        d27 = mt(r"1 =")
        d27.next_to(b27, LEFT)
        self.play(Write(d27))



    def construct(self):
        # play intro animation
        # self.intro()
        # play definitions animation
        # self.definitions()
        # play section 6
        self.the_result()
        self.step_27()