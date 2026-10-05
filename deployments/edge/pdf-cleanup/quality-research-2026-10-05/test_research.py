import unittest, tempfile, os
from pathlib import Path
import pymupdf
from pdf_cleanup.core import cleanup, CleanupError, analyze, validate_output
from pdf_cleanup.native import inspect_pdf

class ResearchTests(unittest.TestCase):
 def setUp(self): self.temp=tempfile.TemporaryDirectory(dir='/out');self.root=Path(self.temp.name)
 def tearDown(self): self.temp.cleanup()
 def create(self,numbers,clipped=False,diagonal=False,real_table=False):
  doc=pymupdf.open()
  for i,n in enumerate(numbers):
   page=doc.new_page(width=612,height=792)
   page.insert_text((72,100),'USEFUL BODY '+str(i),fontsize=11)
   page.insert_text((40,755),n,fontsize=9)
   page.insert_text((350,755),'Footer title',fontsize=8)
   if diagonal or clipped:
    page.draw_line((300,700),(560,790))
    if clipped:
     xref=page.get_contents()[-1]; data=doc.xref_stream(xref)
     # PDF coordinates: visible illustration is clipped above page y=720.
     doc.update_stream(xref,b'q 0 72 612 720 re W n\n'+data+b'\nQ')
   if real_table:
    page.draw_rect(pymupdf.Rect(300,720,560,780))
    page.insert_text((350,738),'REAL TABLE CONTENT',fontsize=10)
  inp=self.root/'input.pdf';doc.save(inp);doc.close();return inp
 def test_clipped_illustration_does_not_prevent_footer_cleanup(self):
  inp=self.create(['1','2'],clipped=True)
  result=cleanup(inp,self.root/'cleaned.pdf')
  self.assertEqual(result['removed_footer_rows'],2)
  with pymupdf.open(self.root/'cleaned.pdf') as doc:
   self.assertIn('USEFUL BODY',doc[0].get_text());self.assertNotIn('Footer title',doc[0].get_text())
 def test_diagonal_illustration_bbox_is_not_a_table(self):
  inp=self.create(['1','2'],diagonal=True)
  result=cleanup(inp,self.root/'cleaned.pdf')
  self.assertEqual(result['removed_footer_rows'],2)
 def test_single_roman_frontmatter_then_decimal_sequence(self):
  inp=self.create(['i','1','2'])
  result=cleanup(inp,self.root/'cleaned.pdf')
  self.assertEqual(result['removed_footer_rows'],3)
 def test_single_decimal_outlier_is_not_silently_removed(self):
  inp=self.create(['99','1','2'])
  with self.assertRaises(CleanupError): cleanup(inp,self.root/'cleaned.pdf')
 def test_table_row_at_confirmed_footer_height_blocks_removal(self):
  inp=self.create(['1','2'],real_table=True)
  with self.assertRaises(CleanupError): cleanup(inp,self.root/'cleaned.pdf')
 def plain(self,name='plain.pdf',fontsize=11,color=(0,0,0),reverse=False,opacity=1):
  doc=pymupdf.open();page=doc.new_page(width=612,height=792)
  pairs=[('A',(72,100)),('B',(72,200))]
  if reverse: pairs.reverse()
  for text,point in pairs: page.insert_text(point,text,fontsize=fontsize,color=color,fill_opacity=opacity)
  path=self.root/name;doc.save(path);doc.close();return path
 def test_no_targets_preserves_exact_pdf_bytes(self):
  inp=self.plain();out=self.root/'cleaned.pdf';result=cleanup(inp,out)
  self.assertEqual(out.read_bytes(),inp.read_bytes())
  self.assertEqual(result['validation'],'passed')
 def verify_change_rejected(self,changed):
  inp=self.plain();native=inspect_pdf(inp)
  with pymupdf.open(inp) as source:
   plan=analyze(source,native)
   with self.assertRaises(CleanupError): validate_output(changed,source,plan,native)
 def test_validation_rejects_changed_font_size_at_same_origin(self):
  self.verify_change_rejected(self.plain('changed.pdf',fontsize=20))
 def test_validation_rejects_changed_text_color(self):
  self.verify_change_rejected(self.plain('changed.pdf',color=(1,0,0)))
 def test_validation_rejects_changed_reading_order(self):
  self.verify_change_rejected(self.plain('changed.pdf',reverse=True))
 def test_validation_rejects_changed_text_opacity(self):
  self.verify_change_rejected(self.plain('changed.pdf',opacity=.2))
 @unittest.expectedFailure  # Explicit unresolved classification risk; never count as passed.
 def test_inline_body_parameter_numbers_are_preserved(self):
  doc=pymupdf.open()
  for n in (1,2):
   page=doc.new_page(width=612,height=792)
   page.insert_text((72,100),'Configuration procedure',fontsize=11)
   page.insert_text((72,180),'The following setting is required:',fontsize=11)
   page.insert_text((72,200),f'Required setting {n}',fontsize=11)
  inp=self.root/'body.pdf';doc.save(inp);doc.close();out=self.root/'cleaned.pdf'
  result=cleanup(inp,out)
  self.assertEqual(result['removed_footer_rows'],0)
  self.assertEqual(inp.read_bytes(),out.read_bytes())
 def test_geometrically_separated_inline_footer_is_cleaned(self):
  doc=pymupdf.open()
  for n in (1,2):
   page=doc.new_page(width=612,height=792)
   page.insert_text((72,100),'USEFUL BODY',fontsize=11)
   page.insert_text((40,755),'Footer title'+' '*55+str(n),fontsize=9)
  inp=self.root/'inline-footer.pdf';doc.save(inp);doc.close()
  result=cleanup(inp,self.root/'cleaned.pdf')
  self.assertEqual(result['removed_footer_rows'],2)
 def test_fallback_preserves_nested_form_body_and_removes_top_level_footer(self):
  from pdf_cleanup.native import remove_text_shows
  form=pymupdf.open();page=form.new_page(width=200,height=200)
  page.insert_text((20,40),'PRESERVE FORM BODY',fontsize=10)
  doc=pymupdf.open()
  for n in (1,2):
   page=doc.new_page(width=612,height=792)
   page.show_pdf_page(pymupdf.Rect(72,72,272,272),form,0)
   page.insert_text((40,755),str(n),fontsize=9)
   page.insert_text((350,755),'Footer title',fontsize=8)
  inp=self.root/'forms.pdf';doc.save(inp);doc.close();form.close()
  native=inspect_pdf(inp)
  with pymupdf.open(inp) as work:
   plan=analyze(work,native)
   xrefs={row[0] for i in range(len(work)) for row in work.get_page_xobjects(i)}
   streams={xref:work.xref_stream(xref) for xref in xrefs}
   remove_text_shows(work,inp,plan)
   self.assertEqual(streams,{xref:work.xref_stream(xref) for xref in xrefs})
   out=self.root/'cleaned.pdf';work.save(out,garbage=2,deflate=True,use_objstms=1)
   with pymupdf.open(inp) as source: validate_output(out,source,plan,native)
  with pymupdf.open(out) as result:
   self.assertIn('PRESERVE FORM BODY',result[0].get_text())
   self.assertNotIn('Footer title',result[0].get_text())
 def test_fallback_refuses_to_guess_targets_inside_a_form(self):
  from pdf_cleanup.native import remove_text_shows
  forms=pymupdf.open();doc=pymupdf.open()
  for n in (1,2):
   page=forms.new_page(width=612,height=792)
   page.insert_text((40,755),str(n),fontsize=9)
   page.insert_text((350,755),'Footer title',fontsize=8)
  # Finish the source before reusing MuPDF's graft map in show_pdf_page().
  for n in (1,2):
   outer=doc.new_page(width=612,height=792)
   outer.show_pdf_page(outer.rect,forms,n-1)
   outer.insert_text((72,100),'PROTECTED BODY',fontsize=11)
  inp=self.root/'nested-footer.pdf';doc.save(inp);doc.close();forms.close()
  original=inp.read_bytes();native=inspect_pdf(inp)
  with pymupdf.open(inp) as work:
   plan=analyze(work,native)
   with self.assertRaisesRegex(ValueError,'no mapped text-show'):
    remove_text_shows(work,inp,plan)
  self.assertEqual(original,inp.read_bytes())
 def test_body_bbox_overlap_uses_operators_and_preserves_body(self):
  doc=pymupdf.open()
  for n in (1,2):
   page=doc.new_page(width=612,height=792)
   page.insert_text((72,100),'Main body',fontsize=11)
   page.insert_text((72,745),'PROTECTED BODY gyp',fontsize=11)
   page.insert_text((40,755),str(n),fontsize=9)
   page.insert_text((90,755),'Footer title',fontsize=9)
  inp=self.root/'overlap.pdf';doc.save(inp);doc.close();out=self.root/'cleaned.pdf'
  result=cleanup(inp,out)
  self.assertEqual(result['cleanup_method'],'text_show_operations')
  with pymupdf.open(out) as output:
   self.assertIn('PROTECTED BODY gyp',output[0].get_text())
   self.assertNotIn('Footer title',output[0].get_text())
 def test_pure_text_footer_form_is_removed_without_changing_its_body_instance(self):
  from pdf_cleanup.native import remove_text_shows
  doc=pymupdf.open();form_xrefs=[]
  for n in (1,2):
   page=doc.new_page(width=612,height=792)
   page.insert_text((40,755),str(n),fontsize=9)
   number_stream=page.get_contents()[0]
   page.insert_text((90,755),'Shared caption',fontsize=9)
   title_stream=page.get_contents()[-1]
   _,resource_ref=doc.xref_get_key(page.xref,'Resources');resources=int(resource_ref.split()[0])
   form_resources=doc.get_new_xref();doc.update_object(form_resources,doc.xref_object(resources))
   xref=doc.get_new_xref();doc.update_object(xref,f'<< /Type /XObject /Subtype /Form /BBox [0 0 612 792] /Resources {form_resources} 0 R >>')
   doc.update_stream(xref,doc.xref_stream(title_stream));form_xrefs.append(xref)
   doc.xref_set_key(resources,'XObject',f'<< /TestForm {xref} 0 R >>')
   stream=doc.get_new_xref();doc.update_object(stream,'<<>>')
   doc.update_stream(stream,b'q 1 0 0 1 0 656 cm /TestForm Do Q\n'+doc.xref_stream(number_stream)+b'\nq /TestForm Do Q\n')
   page.set_contents(stream)
  inp=self.root/'shared-footer-form.pdf';doc.save(inp);doc.close();native=inspect_pdf(inp)
  with pymupdf.open(inp) as work:
   plan=analyze(work,native);before={x:work.xref_stream(x) for x in form_xrefs}
   remove_text_shows(work,inp,plan)
   self.assertEqual(before,{x:work.xref_stream(x) for x in form_xrefs})
   out=self.root/'cleaned.pdf';work.save(out,garbage=2,deflate=True,use_objstms=1)
   with pymupdf.open(inp) as source:validate_output(out,source,plan,native)
  with pymupdf.open(out) as result:self.assertEqual(result[0].get_text().count('Shared caption'),1)

class LegacyOverlapPreservation(unittest.TestCase):
 def test_overlapping_body_is_retained_when_only_footer_operators_are_removed(self):
  import sys
  sys.path.insert(0,'/audit/candidate-v6/tests')
  from test_cleanup import CleanupTests
  fixture=CleanupTests();fixture.setUp()
  try:
   inp=fixture.make_pdf()
   with pymupdf.open(inp) as doc:
    doc[0].insert_text((350,758),'OVERLAPPING BODY',fontsize=12)
    modified=fixture.root/'modified.pdf';doc.save(modified)
   output=fixture.root/'cleaned.pdf';result=cleanup(modified,output)
   self.assertEqual(result['cleanup_method'],'text_show_operations')
   with pymupdf.open(output) as doc:
    self.assertIn('OVERLAPPING BODY',doc[0].get_text())
    self.assertNotIn('Unique title',doc[0].get_text())
  finally:fixture.tearDown()

if __name__=='__main__': unittest.main(verbosity=2)
