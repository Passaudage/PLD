exec(open("../simulateur/Coordonnees.py").read())

def test_string():
	c = Coordonnees(1,1)
	c_str = str(c)
	if(c_str == "(1,1)"):
		print("Test string ok.")
		return True
	else:
		print("Test string ko.")
		return False

def test_abs():
	c = Coordonnees(4,0)
	norme = abs(c)
	if(norme == 4):
		print("Test norme ok.")
		return True
	else:
		print("Test norme ko.")
		return False

def test_div():
	c = Coordonnees(3,3)
	c_str = str(c/3)
	if(c_str == "(1.0,1.0)"):
		print("Test div ok.")
		return True
	else:
		print("Test div ko.")
		return False
		
def test_vectoriel():
	c = Coordonnees(3,4)
	c2 = Coordonnees(3,4)
	vec = c**c2
	if(vec==0):
		print("Test produit vectoriel ok.")
		return True
	else:
		print("Test produit vectoriel ko.")
		return True
	
def test_produit_entier():
	c = Coordonnees(1,1)
	c_str = str(c*3)
	if(c_str == "(3,3)"):
		print("Test produit entier ok.")
		return True
	else:
		print("Test produit entier ko.")
		return False	
		
def test_produit_scalaire():
	c = Coordonnees(1,1)
	c2 = Coordonnees(2,2)
	pd_sca = c*c2
	if(pd_sca == 4):
		print("Test produit scalaire ok.")
		return True
	else:
		print("Test produit scalaire ko.")
		return False	

def test_add():
	c = Coordonnees(1,1)
	c2 = Coordonnees(2,2)
	c_str = str(c+c2)
	if(c_str == "(3,3)"):
		print("Test addition ok.")
		return True
	else:
		print("Test addition ko.")
		return False
		
def test_sub():
	c = Coordonnees(1,1)
	c2 = Coordonnees(2,2)
	c_str = str(c-c2)
	if(c_str == "(-1,-1)"):
		print("Test soustraction ok.")
		return True
	else:
		print("Test soustraction ko.")
		return False
		
def test_se_coupent():
	c1 = Coordonnees(1,1)
	c2 = Coordonnees(4,4)
	c3 = Coordonnees(0,4)
	c4 = Coordonnees(4,0)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ok")
	else:
		print("Test se_coupent ko")
		
def test_se_coupent2():
	c1 = Coordonnees(0,0)
	c2 = Coordonnees(4,0)
	c3 = Coordonnees(0,4)
	c4 = Coordonnees(6,0)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ko")
	else:
		print("Test se_coupent ok")
		
def test_se_coupent3():
	c1 = Coordonnees(0,1)
	c2 = Coordonnees(4,1)
	c3 = Coordonnees(2,4)
	c4 = Coordonnees(2,0)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ok")
	else:
		print("Test se_coupent ko")
		
def test_se_coupent4():
	c1 = Coordonnees(0,1)
	c2 = Coordonnees(4,1)
	c3 = Coordonnees(4,4)
	c4 = Coordonnees(4,0)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ok")
	else:
		print("Test se_coupent ko")
	
def test_se_coupent5():
	c1 = Coordonnees(0,0)
	c2 = Coordonnees(0,4)
	c3 = Coordonnees(0,2)
	c4 = Coordonnees(0,3)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ok")
	else:
		print("Test se_coupent ko")
	
def test_se_coupent6():
	c1 = Coordonnees(0,0)
	c2 = Coordonnees(0,4)
	c3 = Coordonnees(0,2)
	c4 = Coordonnees(0,6)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ok")
	else:
		print("Test se_coupent ko")
	
def test_se_coupent7():
	c1 = Coordonnees(0,0)
	c2 = Coordonnees(0,4)
	c3 = Coordonnees(0,5)
	c4 = Coordonnees(0,6)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ko")
	else:
		print("Test se_coupent ok")
		
def test_se_coupent8():
	c1 = Coordonnees(2,2)
	c2 = Coordonnees(2,4)
	c3 = Coordonnees(2,3)
	c4 = Coordonnees(2,6)
	if(Coordonnees.se_coupent(c1,c2,c3,c4)):
		print("Test se_coupent ok")
	else:
		print("Test se_coupent ko")
	
test_string()
test_abs()
test_div()
test_vectoriel()
test_produit_entier()
test_produit_scalaire()
test_add()
test_sub()
test_se_coupent()
test_se_coupent2()
test_se_coupent3()
test_se_coupent4()
test_se_coupent5()
test_se_coupent6()
test_se_coupent7()

c = Coordonnees(1, 1)
c2 = Coordonnees(2, 1)
c3 = Coordonnees(1, 2)
n_orig = Coordonnees(1, 1)
axe_1 = Coordonnees(0,1)
for co in [c, c2, c3]:
    nc = Coordonnees.changer_repere(co, n_orig, axe_1)
    print(str(co) + " => " + str(nc))
    ac = Coordonnees.inv_changer_repere(nc, n_orig, axe_1)
    print(str(ac) + " <= " + str(nc))
    print("#########")
