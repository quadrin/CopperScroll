// Use the real Sources inspector rather than the retired floating settings card.
export async function openModelSettings(page){
 const settings=page.locator('.map-model-settings');
 if(!await settings.isVisible()){
  const sources=page.getByRole('navigation',{name:'Site reference views'}).getByRole('button',{name:'Sources',exact:true});
  if(await sources.isVisible())await sources.click();
  else{
   const open=page.getByRole('button',{name:'Model & sources',exact:true});
   // At eye level the measurement overlay deliberately hides the compact
   // caption. Leave measurement through its actual toggle to reach settings.
   // checkMeasure explicitly enables it again before making its next picks.
   if(!await open.isVisible()){
    const measure=page.getByRole('button',{name:'Measure',exact:true});
    if(await measure.isVisible()&&await measure.getAttribute('aria-pressed')==='true')await measure.click();
   }
   await open.click();
  }
 }
 await settings.waitFor();
 if(!await settings.evaluate(element=>element.open))await settings.getByText('3D display settings',{exact:true}).click();
 return settings;
}
export async function closeModelSettings(page){
 const close=page.getByRole('button',{name:'Close site reference panel',exact:true});
 if(await close.isVisible())await close.click();
}
export async function chooseModelSetting(page,name){
 const settings=await openModelSettings(page);
 await settings.getByRole('button',{name,exact:true}).click();
}
export async function modelSettingsText(page){
 const settings=await openModelSettings(page),text=await settings.innerText();
 await closeModelSettings(page);
 return text;
}
