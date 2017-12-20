from pythonds.basic.stack import Stack
from pythonds.trees.binaryTree import BinaryTree
import re
import docx
import string
from random import uniform
from collections import defaultdict

def height(tree):
	if tree == None:
		return -1
	else:
		return 1 + max(height(tree.leftChild),height(tree.rightChild))

def set_tree(text):
	wtext = text.split()
	
	pStack = Stack()
	eTree = BinaryTree('')
	pStack.push(eTree)
	currentTree = eTree
	currentTree.insertLeft('')
	currentTree = currentTree.getLeftChild()
	currentTree.setRootVal('1')
	pStack.push(currentTree)

	for i in wtext:
		if BinaryTree.getRootVal(currentTree) == '1' and not currentTree.isLeaf():
			currentTree = pStack.pop()
			currentTree.insertRight('')
			currentTree = currentTree.getRightChild()
			currentTree.setRootVal('2')
			pStack.push(currentTree)
		if i == '(':
			currentTree.insertLeft('')
			pStack.push(currentTree)
			currentTree = currentTree.getLeftChild()
		elif i not in ['(',')']:
			if currentTree.isLeaf():
				if BinaryTree.getRootVal(currentTree) != '' :
					currentTree = pStack.pop()
					currentTree.insertRight('')
					currentTree = currentTree.getRightChild()
					currentTree.setRootVal(i)
				elif BinaryTree.getRootVal(currentTree) != None:
					currentTree.setRootVal(i)
				pStack.push(currentTree)
		elif i == ')':
			currentTree = pStack.pop()
			currentTree = pStack.pop()
		else:
			raise ValueError
	return eTree

def extract_heading(doc_name):
	f = open(doc_name, 'rb')
	#print(f)
	document = docx.Document(f)
	f.close()
	d1 = []
	for h in document.paragraphs:
		if ('Heading') in h.style.name:	
			d1.append(h.text.lower().strip())
	d_test = d1
	ref1={}
	k = 1
	k1 = 0
	ref1['headings'] = {}
	head = 1
	for d in d_test:
		idd = 'id' + str(k)
		if d[0].isdigit(): 
			if d[0][0] != head:
				k1 += 1
				idd1 = 'idd' + str(k1)
				k = 1
				head = d[0][0]
			if d[1] != '.':
				
				ref1['headings'][idd1] = {}
				ref1['headings'][idd1]['num_chapter'] = d[0][0]
				ref1['headings'][idd1]['name_chapter'] = d[1:]
				ref1['headings'][idd1]['sub'] = {}
			else:
				ref1['headings'][idd1]['sub'][idd] = {}
				ref1['headings'][idd1]['sub'][idd]['sub_name'] = re.sub(r'[^\w\s]+|[\d]+', r'',d)
				k += 1
		else:
			pass
	return ref1

referat = ''
def preorder1(tree, chapters):
	global referat
	if tree.key == '$':
		referat += chapters['num_chapter'] + ' '
	elif tree.key == '*':
		referat +=  chapters['name_chapter']
		referat += '. '
	elif tree.key == '**':
		for i in chapters['sub']:
			referat +=  chapters['sub'][i]['sub_name'].lower() + ', '
		referat = referat[:len(referat)-2]
		referat += '. '
	else:
		if tree.key != None and str(tree.key) not in ['1', '2'] and tree.key != '':
			referat += tree.key + ' '
		else:
			pass

	if tree.leftChild:
		preorder1(tree.leftChild, chapters)
	if tree.rightChild:
		preorder1(tree.rightChild, chapters)
	return referat.capitalize()


def create_referat(file):
	text1 = '( В ( главе ( $ ( рассматривается ( * ) ) ) ) ) ( Освещаются ( такие вопросы ( как: ( ** ) ) ) )'
	
	eTree1 = set_tree(text1)
	dict1 = extract_heading('/upload/' + file[5])

	for i in ['idd1', 'idd2', 'idd3', 'idd4', 'idd5']:
		try:
			for strk in ['лит','библ', 'прилож', 'источники', 'заключен', 'вывод']:
				if  dict1['headings'][i]['name_chapter'].find(strk) == 1:
					i = 0
			preorder1(eTree1, dict1['headings'][i])
		except:
			pass
	return referat
	

if __name__ == '__main__':
	create_referat('/media/share/ANALIZ_INTELLECT/vkr.docx')
