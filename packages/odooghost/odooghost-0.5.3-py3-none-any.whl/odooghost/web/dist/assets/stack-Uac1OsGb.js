import{g as e}from"./VWarningAlert-RzhqZRjB.js";const t=e`
  query getStack($name: String!) {
    stack(name: $name) {
      name
      state
      odooVersion
      dbVersion
      networkMode
      containers {
        id
        name
        image
        service
        state
      }
    }
  }
`,s=e`
  query getStacks {
    stacks {
      name
      state
      odooVersion
      dbVersion
    }
  }
`,n=e`
  query getContainers {
    containers {
      id
      name
      image
      service
      state
    }
  }
`;export{s as Q,t as a,n as b};
