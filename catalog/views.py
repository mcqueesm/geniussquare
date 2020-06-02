import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot
from django.shortcuts import render
from django.views.generic import TemplateView
import dance.pentomino as pentomino
import dance.dance as dance
from catalog.forms import IndexForm
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import random


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

        snum = None
        source = 1
        try:
            snum = self.solve(text)
        except ValueError:
            source = 2

    
        
        paths = [
            'solutions0.png',
            'solutions1.png',
            'solutions2.png',
            'solutions3.png',
            'solutions4.png',
            'solutions5.png',
            'solutions6.png',
            'solutions7.png',
            'solutions8.png',
            'solutions9.png'

        ]
        args = {'form': form, 'source': source, 'number': snum, 'paths': paths}
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
        solset = random.sample(solution, 10)
        print('solset length is ', len(solset))
        snum = len(solution)
        
        
        #fig.suptitle('Number of solutions for \n {s}: \n {t}'.format(s= dice, t=snum), fontsize=40)
        for i, x in enumerate(solset):
            fig = matplotlib.pyplot.figure()
            pentomino.display_solution(b, x, i, fig)
            matplotlib.pyplot.close()
        
        
        #pdf = PdfPages('catalog/static/solutions.pdf')
        #pdf.savefig()

        #pdf.close()
        return snum
        
