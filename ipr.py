def calculate_pi(q_test, pr, pwf_test):
    """Productivity Index (PI) for a test point"""
    return q_test / (pr - pwf_test)

def vogel_ipr(qmax, pr, pwf):
    """Vogel IPR model for oil wells"""
    x = pwf / pr
    return qmax * (1 - 0.2 * x - 0.8 * x**2)

def fetkovich_ipr(pi_eff, pr, pwf, n):
    """Fetkovich IPR model"""
    return pi_eff * (pr**n - pwf**n)

def adjust_pi_for_skin(pi, skin):
    return pi / (1 + skin)

def ipr_comparison():
    print("\n--- Inflow Performance Relationship (IPR) Tool ---")
    
    pr = float(input("Enter reservoir pressure, Pr (psi): "))
    pwf_test = float(input("Enter test bottom-hole pressure, Pwf_test (psi): "))
    q_test = float(input("Enter test flow rate at Pwf_test (STB/day): "))
    skin = float(input("Enter skin factor (S): "))
    n = float(input("Enter flow exponent (n, 1 for oil, <1 for gas): "))

    # Calculate PI and adjust for skin
    pi = calculate_pi(q_test, pr, pwf_test)
    pi_eff = adjust_pi_for_skin(pi, skin)

    # Estimate q_max from Vogel
    x = pwf_test / pr
    q_max = q_test / (1 - 0.2 * x - 0.8 * x ** 2)

    print("\nPwf (psi) | Vogel (STB/day) | Fetkovich (STB/day)")
    print("--------------------------------------------------")
    step = int(pr / 6)
    for pwf in range(0, int(pr) + 1, step):
        q_vogel = vogel_ipr(q_max, pr, pwf)
        q_fetkovich = fetkovich_ipr(pi_eff, pr, pwf, n)
        print(f"{pwf:<10} | {round(q_vogel, 2):<17} | {round(q_fetkovich, 2)}")

    print("\n--- Summary ---")
    print(f"Calculated PI: {round(pi, 2)} STB/day/psi")
    print(f"Adjusted PI with skin (S={skin}): {round(pi_eff, 2)} STB/day/psi")
    print(f"Estimated q_max from Vogel: {round(q_max, 2)} STB/day")

# Run the tool
ipr_comparison()
