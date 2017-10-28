# MySQL Workbench Plugin - Written in MySQL Workbench 6.3.9
# Created by Ian Welerson - https://github.com/ianwelerson/MWB-DBDocPy
# Based on the script created by Rodrigo Schmidt Nurmberg - https://github.com/rsn86/MWB-DBDocPy

from wb import *
import grt
from mforms import FileChooser
import mforms

ModuleInfo = DefineModule(name="DDictionary", author="Ian Welerson", version="1.0", description="Data Dictionary")

@ModuleInfo.plugin("ianwelerson.DDictionary", caption="DDictionary: Diagram Data in HTML", description="Create a data dictionary from a diagram", input=[wbinputs.currentCatalog()], pluginMenu="Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def htmlDataDictionary(catalog):
  htmlOut = ""
  filechooser = FileChooser(mforms.SaveFile)
  if filechooser.run_modal():
    htmlOut = filechooser.get_path()
    print "HTML File: %s" % (htmlOut)
  if len(htmlOut) <= 1:
    return 1

  # iterate through columns from schema
  schema = catalog.schemata[0]
  htmlFile = open(htmlOut, "w")
  print >>htmlFile, "<html><head>"
  print >>htmlFile, "<title>Dicionario de dados de %s</title>" % (schema.name)
  print >>htmlFile, """<style>
    td,th {
      vertical-align:middle;
    }
    table {
      border-collapse: collapse;
    }
    caption, th, td {
      padding: .2em .8em;
      border: 1px solid #000;
    }
    caption {
      background: #dadada;
      font-weight: bold;
      font-size: 1.1em;
    }
    th {
      font-weight: bold;
      background: #dadada;
    }
    td {
      background: #FFF;
    }
    .column-infos {
      text-align: center;
    }
  </style>
</head>
<body>"""
  for table in schema.tables:
    print >>htmlFile, "<table><caption>Tabela: %s</caption>" % (table.name)
    print >>htmlFile, """
<tr>
<th>Nome</th>
<th>NN</th>
<th>PK</th>
<th>FK</th>
<th>Descricao</th>
</tr>"""
    for column in table.columns:
      pk = ('', 'X')[bool(table.isPrimaryKeyColumn(column))]
      fk = ('', 'X')[bool(table.isForeignKeyColumn(column))]
      nn = ('', 'X')[bool(column.isNotNull)]
      print >>htmlFile, "<tr><td>%s</td><td class='column-infos'>%s</td><td class='column-infos'>%s</td><td class='column-infos'>%s</td><td>%s</td></tr>" % (column.name,nn,pk,fk,column.comment)
    print >>htmlFile, "</table></br>"
  print >>htmlFile, "</body></html>"
  return 0
