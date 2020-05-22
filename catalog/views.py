import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot
from django.shortcuts import render
from django.views.generic import TemplateView
import catalog.dance.pentomino as pentomino
import catalog.dance.dance as dance
from catalog.forms import IndexForm
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Create your views here.
# Render the HTML template index.html with the data in the context variable

class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        form = IndexForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = IndexForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
       
        snum = self.solve(text)
        args = {'form': form, 'source': True, 'number': snum}
        return render(request, self.template_name, args)

    def solve(self, dice):
        numDic = {
        'A': 0,
        'B': 1,
        'C': 2, 
        'D': 3,
        'E': 4,
        'F': 5
        }
        
        dlist = dice.split()
        b = np.copy(pentomino.boards['hollow_chess_board'])
        for x in dlist:
            b[int(numDic[x[0]]), int(x[1])-1] = 0

        np.savetxt('sub_problem_1', pentomino.exact_cover_problem(b).astype(np.int), fmt='%r')
        mat = np.loadtxt('sub_problem_1')
        dl = dance.DancingLinks(mat)
        solution = dl.generate_all_solutions()
        snum = len(solution)
        cols = 5
        #rows = 20
        rows = snum//cols+1
        fig = matplotlib.pyplot.figure(figsize=(8, rows*2))
        fig.tight_layout()
        #fig.suptitle('Number of solutions for \n {s}: \n {t}'.format(s= dice, t=snum), fontsize=40)
        for i in range(1, snum+1):
            print("in for loop ", i)
            pentomino.display_solution(b, solution[i-1], fig, rows, cols, i)
        
        fig.savefig("catalog/static/solutions.pdf", bbox_inches = 'tight', pad_inches = 0)
        #pdf = PdfPages('catalog/static/solutions.pdf')
        #pdf.savefig()

        #pdf.close()
        return snum
        
