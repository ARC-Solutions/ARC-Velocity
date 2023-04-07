import React, {createContext} from "react";
import { Content } from "./Content";
import {InfoSection} from "./InfoSection"
import { ActionSection } from "./ActionSection";
export const AppContext = createContext();
function App() {
  return (
   <AppContext.Provider value = {AppContext}>
    <main id="landing-page">
    <div className="container content">
      <Content/>
    </div>
    </main>

    <section id="project-page">
      <InfoSection/>
      <ActionSection/>
    </section>
   </AppContext.Provider>
  );
}

export default App;
