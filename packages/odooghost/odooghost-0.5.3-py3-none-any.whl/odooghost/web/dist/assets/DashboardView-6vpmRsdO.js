import{g as i}from"./VWarningAlert-RzhqZRjB.js";import{_ as c}from"./VContainers-HbY9noeu.js";import{_ as l,a as u}from"./VHeader-aJjdxqCh.js";import{_ as a}from"./VStat-OojnLe6b.js";import{u as _,o as m,c as d,a as e,w as f,b as s,d as o}from"./index-7bE_XEN1.js";import"./VErrorAlert-q8fIVpmi.js";const p=i`
  query getDashboard {
    version
    dockerVersion
    stackCount
    containers(stopped: false) {
      id
      name
      image
      service
      state
    }
  }
`,g={class:"mx-auto max-w-7xl"},h={class:"grid grid-cols-1 gap-4 sm:grid-cols-3"},k=o("h3",null,"Running Containers",-1),y={__name:"DashboardView",setup(v){const{result:t,loading:r,error:n}=_(p);return(x,D)=>(m(),d("div",null,[e(u,{title:"Dashboard"}),e(l,{loading:s(r),error:s(n),result:s(t),"result-key":"version"},{default:f(()=>[o("section",null,[o("div",g,[o("div",h,[e(a,{name:"Odooghost version",stat:s(t).version},null,8,["stat"]),e(a,{name:"Docker version",stat:s(t).dockerVersion},null,8,["stat"]),e(a,{name:"Stacks count",stat:s(t).stackCount},null,8,["stat"])])])]),o("section",null,[k,e(c,{containers:s(t).containers},null,8,["containers"])])]),_:1},8,["loading","error","result"])]))}};export{y as default};
