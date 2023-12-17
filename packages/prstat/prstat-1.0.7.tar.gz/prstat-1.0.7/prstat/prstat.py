"""
import sympy as sp는 미리 선언 되어있습니다.
사용할땐 from prstat.prstat import * 하시면 됩니다.
function의 미지수는 가능하면 x로 통일해주세요
참고로 e를 제외한 a-z는 symbol로 설정되어 있으며 e는 자연로그의 밑 e로 선언되어있습니다.
"""
import sympy as sp
import numpy as np
from numpy.linalg import matrix_power
from fractions import Fraction as frac
a,b,c,d,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z=sp.symbols("a b c d f g h i j k l m n o p q r s t u v w x y z")
lamb=sp.Symbol('λ')

e=sp.E
pi=sp.pi
inf=sp.oo

symbol=sp.Symbol
exp=sp.exp 
lim=sp.limit
log=sp.log
diff=sp.diff
integral=sp.integrate
solve=sp.solve
branch=sp.Piecewise
sigma=sp.summation
expand=sp.expand

def plot(function,min=-10,max=10):
    """
    함수를 그래프로 보여주는 함수
    """
    sp.plot(function,(x,min,max),axis_center=(0,0))
    return

def unit(function):
    """
    unit step function 입니다. 곱하기가 아닌 unit(function)으로 사용합니다.
    """
    return function * sp.Heaviside(function, 1)

def fact(n):
    """
    팩토리얼입니다. 내장함수로 제작되었으므로 import 하지마세요
    """
    try:
        ret=1
        for i in range(1,n+1):
            ret*=i
        return ret
    except:
        return sp.factorial(n)

def comb(n,r):
    """
    조합입니다. 혹시나 컴퓨터에 파이썬 버전이 낮을경우를 대비해 내장함수로 제작하였습니다.
    """
    return fact(n)//(fact(r)*fact(n-r))

def multi_comb(n,r):
    """
    구분하는 단위가 n입니다. 만약 (x+y+z)=6의 자연수 해의 쌍은 3H9이니 multi_comb(3,9)로 나타낼 수 있습니다.
    """
    return comb(n+r-1,r) 

def pr_b_a(pr_a_b,pr_a,pr_b):
    """
    활용예시 : pr_s_k=pr_b_a(pr_k_s,pr_s,pr_k) 즉 인자는 뒤집은것, 원래함수의 | 앞에있는것, 원래함수의 | 뒤에있는것 순서로 씁니다.
    """
    return pr_a_b*pr_a/pr_b 

bayes=pr_b_a

def communication_system(pr_0t, pr_1t, pr_0r_0t, pr_1r_0t, pr_0r_1t, pr_1r_1t):
    """
    Pr(0received|0transmitted)하는 문제입니다. 입력 : pr_0t, pr_1t, pr_0r_0t, pr_1r_0t, pr_0r_1t, pr_1r_1t 
    """
    pr_0r = (pr_0r_0t * pr_0t) + (pr_0r_1t * pr_1t)
    pr_1r = (pr_1r_0t * pr_0t) + (pr_1r_1t * pr_1t)
    
    pr_1t_0r = pr_b_a(pr_0r_1t,pr_1t,pr_0r)
    pr_0t_1r = pr_b_a(pr_1r_0t,pr_0t,pr_1r)
    
    pr_error= (pr_0r_1t * pr_1t) + (pr_1r_0t * pr_0t)
    
    print(f"pr_0r={pr_0r}")
    print(f"pr_1r={pr_1r}")
    print(f"pr_1t_0r={pr_1t_0r}")
    print(f"pr_0t_1r={pr_0t_1r}")
    print(f"pr_error={pr_error}")
    return(pr_0r,pr_1r,pr_1t_0r,pr_0t_1r,pr_error)

def digital_communication(n,k,t,p):
    """
    디지털통신에서 codeword 수신 실패하는 문제입니다. 입력형식 : n,k,t,p
    """
    pr_ok = 0
    for i in range(t+1) :
        pr_ok += comb(n,i) * (p**i) * ((1-p)**(n-i))
    print(f"Pr_error : {1-pr_ok}")
    return (1-pr_ok)

def light_bulb_manufacturer(La,Sa,pr_l,pr_s,k,equ=None):
    """
    전구수명찾는 문제입니다. 입력형식 : L타입a, S타입a, L타입확률, S타입확률, k시간, 방정식(디폴트는(1-a)*(a**k))을 받습니다.
    """
    if not equ:
        equ=(1-a)*(a**k)
    try:
        pr_k_s=equ.subs(a,Sa)
        pr_k_l=equ.subs(a,La)
    except:
        print("""방정식 형식이 올바르지 않습니다. 방정식 생성 예시
a=sp.Symbol('a')
equ=(1-a)*(a**k)
              """)
        return
    pr_k= (pr_k_s*pr_s)+(pr_k_l*pr_l)
    
    pr_s_k=pr_b_a(pr_k_s,pr_s,pr_k)
    pr_l_k=pr_b_a(pr_k_l,pr_l,pr_k)
    
    pr_error=pr_l_k

    print(f"pr_k_s : {pr_k_s}")
    print(f"pr_k_l : {pr_k_l}")
    print(f"pr_s_k : {pr_s_k}")
    print(f"1-pr_l_k : {1-pr_l_k}")
    if pr_s_k>pr_l_k:
        print("S type일것이라고 추측가능")
    else:
        print("L type일것이라고 추측가능")    
    print(pr_error)
    return

def what_is_PMF():
    print("PMF stands for Probability Mass Function and usually notated as PX(k). It is used to describe probabilisitc characteristics of a discrete random variable.")
def what_is_CDF():
    print("CDF stands for Cumulative Distribution Function and usually notated as FX(x). It is used to describe probabilisitc characteristics of a both discrete and continuous random variable.")
def what_is_PDF():
    print("PDF stands for Probability Density Function and usually notaed as fx(x). It is used to describe probability characteristics of a continuous random variable.")

def auditorium_row_seat(row,seat,max_row,zero_row_seat=10):
    """
    Row1=11seats와 같이 강당그림이 그려진 문제입니다.
    """
    row_seat=row+zero_row_seat #해당 row의 자리 개수
    if seat>row_seat:
        pr_s_r=0
    else:
        pr_s_r=1/row_seat
    
    pr_s=0
    for r in range(1,max_row+1):
        row_seat=r+zero_row_seat
        pr_s+=frac((seat<=row_seat),row_seat)/max_row
    
    pr_r=1/max_row
    pr_r_s=pr_b_a(pr_s_r,pr_r,pr_s)
    
    print(pr_s_r)
    print(pr_r_s)
    return

def is_CDF(function):
    """
    CDF인지 판단해주는 함수. 음의무한대극한이 0이고, 무한대극한이 1이고, 감소하지않으며, 연속이여야합니다.
    """
    plot(function)
    error=0
    try:
        if lim(function,x,-inf)!=0:
            print("음의 무한대 극한 0 아님")
            return 0
        else:
            print("음의 무한대 극한 0")
    except:
        print("음의 무한대 극한 확인불가")
        error=1
    try:
        if lim(function,x,inf)!=1:
            print("양의 무한대 극한 1 아님")
            return 0
        else:
            print("양의 무한대 극한 1")
    except:
        print("양의 무한대 극한 확인불가")
        error=1
    try:
        tmp=sp.Symbol('tmp')
        if sp.simplify(lim(function,x,tmp,'+')-lim(function,x,tmp,'-'))!=0:
            print("연속아님")
            return 0
        else:
            print("연속")
    except:
        print("연속확인불가")
        error=1
    try:
        diff_x=diff(function,x)
        if sp.solveset(diff_x<0, domain=sp.S.Reals).is_empty!=1:
            print("감소구간확인")
            return 0
        else:
            print("감소구간없음")
    except:
        print("감소 확인 불가")
        error=1

    if error:
        print("에러가 감지되었습니다. 그래프를 보고 알아서 판단하세요.")
        return -1
    else:
        return 1

def find_c_PDF(function,min=-inf,max=inf):
    return solve(integral(function, (x, min, max)) - 1, c)[0]

def find_c_PMF(function):
    return sp.solve(sp.summation(function,(n,1,inf))-1,c)[0]

def Ex_PDF(function,min=-inf,max=inf):
    c_value = solve(integral(function, (x, min, max)) - 1, c)[0]
    expectation = integral(x * function.subs(c, c_value), (x, min, max))
    return expectation

def Ex_PMF(function, min,max):
    interval=sp.Interval(min,max)
    c_value = sp.solveset(sp.summation(function, (x, interval.start, interval.end)) - 1, c).args[0]
    expectation = sp.summation(x * function.subs(c, c_value), (x, interval.start, interval.end))
    return expectation

def Ex_CDF(function, min_value, max_value):
    print("검증안됌.")
    interval = sp.Interval(min_value, max_value)
    expectation = sp.summation(x * (function - function.subs(x, x - 1)), (x, interval.start, interval.end))
    return expectation

def game_of_chance(num_games,win_rate,A_lose,A_win):
    """
    과제2
    게임수, 승률, A가잃는돈, A가얻는돈. 잃는돈이 먼저임을 주의!!!
    예시 : print(game_of_chance(10,frac(1,3),1,3))
    """
    win_prob_A = win_rate
    loss_prob_A = 1 - win_prob_A
    win_amount_A = A_win
    loss_amount_A = -A_lose
    expected_winnings_A = num_games * (win_prob_A * win_amount_A + loss_prob_A * loss_amount_A)
    return expected_winnings_A

def Ex_and_var(f, Ex, var):
    """
    과제3
    상수는 그대로 더함 일차항은 Ex와 같음 이차항은 var+Ex**2랑 같음
    """
    f=sp.expand(f)
    a = f.coeff(x, 2)
    b = f.coeff(x, 1)
    c = f.coeff(x, 0)
    E_f = (c) + (b * Ex) + (a * (var+Ex*Ex))
    return E_f

def nth_moment_poisson(function, n, m_min, m_max):
    """
    과제4
    예시 입력
    f= (lamb**m) * exp(-lamb) / fact(m)
    print(nth_moment_poisson(f,3,0,inf))
    """
    moment = sp.summation(function.subs(m, m).subs(lamb, lamb) * (m**n), (m, m_min, m_max))
    return expand(moment)

def phi_x(Ef, pdf):
    """
    구현이 너무 어렵습니다... 포기
    """
    return "포기, 5,6,7안함"

def calculate_statistics(cdf):
    """
    과제8
    CDF를 분석해주는 함수
    cdf = branch((0,x<0),(x*x,(0<=x) & (x<=1)),(1,x>1))
    print(calculate_statistics(cdf))
    평균(mean),분산(var),왜도(skewness),첨도(kurtosis) 순서
    """
    mean = sp.integrate(x * sp.diff(cdf, x), (x, -sp.oo, sp.oo))
    variance_expr = sp.integrate((x - mean)**2 * sp.diff(cdf, x), (x, -sp.oo, sp.oo))
    variance = sp.simplify(variance_expr)
    third_moment = sp.integrate((x - mean)**3 * sp.diff(cdf, x), (x, -sp.oo, sp.oo))
    skewness = sp.simplify(third_moment / variance**(3/2))
    fourth_moment = sp.integrate((x - mean)**4 * sp.diff(cdf, x), (x, -sp.oo, sp.oo))
    kurtosis = sp.simplify((fourth_moment / variance**2))

    return map(float,[mean, variance, skewness, kurtosis])

def markov_chain(n,start,arr):
    """
    pi_n에서 n값, 어디서 시작했는지, 배열에 관한정보 과제 16번
    """
    return matrix_power(arr,n)[start-1]

if __name__ == "__main__":
    arr=np.array([[0.3,0.5,0.2],[0.3,0.5,0.2],[0.3,0.5,0.2]])
    print(markov_chain(2,3,arr))