from pdext import pd 

pd.ext.install_extension('circle_calculations', 'github:connectedblue/pdext_collection',collection='demo')
x = pd.DataFrame({'radius':[1,2,3,4]})

x.ext.demo.circle_calculations()