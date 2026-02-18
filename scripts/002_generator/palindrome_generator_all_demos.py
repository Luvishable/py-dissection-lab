"""
Palindrome generator demo pack (yield / next / send / close / throw)
"""

from __future__ import annotations


def is_palindrome(num: int) -> bool:
    """
    Arithmetic palindrome check, single-digit numbers are not considered.
    """
    if num < 10:
        return False

    original = num
    reversed_num = 0

    while num > 0:
        digit = num % 10
        reversed_num = reversed_num * 10 + digit
        num //= 10

    return original == reversed_num


def infinite_palindromes():
    """
    Infinite palindrom generator.

    Key line: jump = (yield num)
    This line does two things:
    1) yield num -> outputs a palindrome to the caller and pauses here.
    2) When resumed:
        - if resumed by next(gen) / for-loop -> (yield num) evaluates to None
        - if resumed by gen.send(X)          -> (yield num) evaluates to X

    Therefore jump can be None or and int.
    If jump is an int, we jump the internal search state to that number which is X in this case.
    """

    num = 0

    try:
        while True:
            if is_palindrome(num):
                # Parantheses are not required; they are used to emphasize that
                # 'yield num' is an expression whose result is assigned to 'jump'
                jump = (yield num)

                # 'jump' is not "num"; it's whatever the caller sent via .send()
                # - next() / for => jump becomes None
                # - send(1000) => jump becomes 1000
                if jump is not None:
                    # Jump the search: continue scanning from the provided value
                    num = jump

            # Normal progression (or after a jump): move forward
            num += 1

    finally:
        # Runs on close(), or if generator exits due to an exception.
        print("[cleanup] infinite_palindromes is closing (finally block executed).")

# ----------------------------------------------------------------------
# DEMO A: next() causes the yield-expression result to become None
# ----------------------------------------------------------------------
def demo_next_makes_jump_none():
    print("\n=== DEMO A: next() resumes -> yield-expression result becomes None ===")

    gen = infinite_palindromes()

    # First palindrome: generator runs until it hits the first 'yield num'
    p1 = next(gen)
    print("next(gen) ->", p1)

    # next(gen) resumes the generator WITHOUT sending a value.
    # Therefore inside the generator: jump = (yield num) becomes jump = None.
    p2 = next(gen)
    print("next(gen) ->", p2)

    # Cleanup
    gen.close()


# ----------------------------------------------------------------------
# DEMO B: send() jump (the "correct" usage pattern)
# ----------------------------------------------------------------------
def demo_send_jump_correct():
    print("\n=== DEMO B: send() can 'jump' the internal search state (correct pattern) ===")

    gen = infinite_palindromes()

    # When generator didn't start, you can not give it a value via send(). Thus, you must start it first via next()
    p = next(gen)
    print("First palindrome via next(gen) ->", p)

    # send(X) does two things:
    # 1) resumes the generator and injects X as the result of (yield num)
    # 2) returns the NEXT yielded palindrome after the generator continues running
    jump_to = 100
    p = gen.send(jump_to)
    print(f"gen.send({jump_to}) ->", p)

    jump_to = 1000
    p = gen.send(jump_to)
    print(f"gen.send({jump_to}) ->", p)

    # Demonstrate that send(None) behaves like next(gen) in terms of injection
    p = gen.send(None)
    print("gen.send(None) ->", p)

    gen.close()


# ----------------------------------------------------------------------
# DEMO C: for + send can "skip" values if you ignore send() return
# ----------------------------------------------------------------------
def demo_for_plus_send_can_skip():
    print("\n=== DEMO C: mixing for-loop + send() can skip outputs if send() return is ignored ===")

    gen = infinite_palindromes()

    # for-loop calls next(gen) each iteration.
    # If inside the loop you ALSO call gen.send(...), that advances the generator again.
    # If you don't capture the return value of send(), you effectively "skip" a palindrome.
    for idx, p in enumerate(gen, start=1):
        print(f"[for] {idx}. palindrome:", p)

        digits = len(str(p))
        jump_to = 10 ** digits

        # send() returns the next yielded palindrome.
        # If you ignore this return, you won't see this palindrome printed anywhere.
        returned_by_send = gen.send(jump_to)
        print(f"    [send({jump_to}) returned] {returned_by_send}")

        if idx >= 3:
            gen.close()
            break

    print("Note: If you use for + send, ALWAYS handle the return of send().")


# ----------------------------------------------------------------------
# DEMO D: throw() and close() behavior (separate from the combined demo)
# ----------------------------------------------------------------------
def demo_throw_and_close():
    print("\n=== DEMO D: throw() and close() behavior ===")

    gen = infinite_palindromes()

    try:
        p = next(gen)
        print("next(gen) ->", p)

        # throw() injects an exception at the paused yield point
        print("Injecting ValueError into generator with throw() ...")
        gen.throw(ValueError("Stop here via throw()"))

    except ValueError as e:
        print("Caught outside:", repr(e))

    # Generator may already be terminated; create a fresh one
    gen2 = infinite_palindromes()
    print("next(gen2) ->", next(gen2))

    print("Now closing gen2 via close() ...")
    gen2.close()

    # After close, next/send raises StopIteration
    try:
        next(gen2)
    except StopIteration:
        print("After close(): next(gen2) -> StopIteration (expected)")

    try:
        gen2.send(1000)
    except StopIteration:
        print("After close(): gen2.send(1000) -> StopIteration (expected)")



def main():
    # Run all demos in a sensible order:
    demo_send_jump_correct()


if __name__ == "__main__":
    main()
