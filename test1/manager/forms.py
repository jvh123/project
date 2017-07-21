from django import forms
class SearchForm(forms.Form):
    Search= forms.CharField(
      required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
   )
class PlanForm(forms.Form):
    CHOICES1 = [('number_1q2002', '1q2002'), ('number_2q2002', '2q2002'), ('number_3q2002', '3q2002'), ('number_4q2002', '4q2002'),
                ('number_1q2003', '1q2003'), ('number_2q2003', '2q2003'), ('number_3q2003', '3q2003'), ('number_4q2003', '4q2003'),
                ('number_1q2004', '1q2004'), ('number_2q2004', '2q2004'), ('number_3q2004', '3q2004'), ('number_4q2004', '4q2004'),
                ('number_1q2005', '1q2005'), ('number_2q2005', '2q2005'), ('number_3q2005', '3q2005'), ('number_4q2005', '4q2005'),
                ('number_1q2006', '1q2006'), ('number_2q2006', '2q2006'), ('number_3q2006', '3q2006'), ('number_4q2006', '4q2006'),
                ('number_1q2007', '1q2007'), ('number_2q2007', '2q2007'), ('number_3q2007', '3q2007'), ('number_4q2007', '4q2007'),
                ('number_1q2008', '1q2008'), ('number_2q2008', '2q2008'), ('number_3q2008', '3q2008'), ('number_4q2008', '4q2008'),
                ('number_1q2009', '1q2009'), ('number_2q2009', '2q2009'), ('number_3q2009', '3q2009'), ('number_4q2009', '4q2009'),
                ('number_1q2010', '1q2010'), ('number_2q2010', '2q2010'), ('number_3q2010', '3q2010'), ('number_4q2010', '4q2010'),
                ('number_1q2011', '1q2011'), ('number_2q2011', '2q2011'), ('number_3q2011', '3q2011'), ('number_4q2011', '4q2011'),
                ('number_1q2012', '1q2012'), ('number_2q2012', '2q2012'), ('number_3q2012', '3q2012'), ('number_4q2012', '4q2012'),
                ('number_1q2013', '1q2013'), ('number_2q2013', '2q2013'), ('number_3q2013', '3q2013'), ('number_4q2013', '4q2013'),
                ('number_1q2014', '1q2014'), ('number_2q2014', '2q2014'), ('number_3q2014', '3q2014'), ('number_4q2014', '4q2014'),
                ('number_1q2015', '1q2015'), ('number_2q2015', '2q2015'), ('number_3q2015', '3q2015'), ('number_4q2015', '4q2015'),
                ('number_1q2016', '1q2016'), ('number_2q2016', '2q2016'), ('number_3q2016', '3q2016')]
    Plan1=forms.ChoiceField(widget=forms.RadioSelect() ,choices=CHOICES1)


