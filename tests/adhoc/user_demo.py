from pdext import pd 

pd.ext.import_extension('github:connectedblue/pdext_collection -> demo.circle_calculations')
x = pd.DataFrame({'radius':[1,2,3,4]})

x.ext.demo.circle_calculations()