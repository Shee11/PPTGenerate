
import json
import re
import os

mdx_path = "/Users/zhang11/Downloads/slides (6).mdx"
output_dir = "output/render_test"
output_state = os.path.join(output_dir, "state.json")

def create_mock_component(name):
    return f"""
import React from 'react';

export const {name} = (props: any) => {{
    return (
    <div className="p-4 border-2 border-dashed border-gray-600 bg-gray-800 rounded-lg my-4">
        <div className="text-yellow-400 font-bold mb-2">&lt;{name} /&gt; (Mock Render)</div>
        <pre className="text-xs text-green-400 mt-2 overflow-auto max-h-60">
        {{JSON.stringify(props, null, 2)}}
        </pre>
    </div>
    );
}};
"""

surface_cluster_map_code = """
import React from 'react';
import { motion } from 'framer-motion';
import * as Lucide from 'lucide-react';

// Use destructuring for cleaner code, assuming shim provides the module
const { Users, AlertCircle, ArrowRight, Database, Settings, Brain } = Lucide;

export const SurfaceClusterMap = (props) => {
  // Destructure props safely
  const surfaces = props.surfaces || [];
  const problems = props.problems || [];
  const target_state = props.target_state || { personalization: [] };

  return (
    <div className="p-6 bg-slate-900/50 rounded-xl border border-slate-700 font-sans text-slate-100 my-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
        {/* Left: Current Surfaces */}
        <div className="space-y-4">
          <h3 className="text-xs uppercase tracking-wider text-slate-400 font-bold mb-2 border-b border-slate-700 pb-2">
            Current: Fragmented
          </h3>
          <div className="space-y-2">
            {surfaces.map((s, i) => (
              <motion.div 
                key={s.id || i}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: i * 0.1 }}
                className="p-3 bg-slate-800 rounded-lg border border-slate-600 flex justify-between items-center shadow-sm"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-200">{s.label}</div>
                  <div className="text-[10px] text-slate-500 uppercase">Owner: {s.owner}</div>
                </div>
                <Users size={14} className="text-slate-500" />
              </motion.div>
            ))}
          </div>
          
          {/* Problems Overlay */}
          <div className="mt-4 bg-red-950/30 border border-red-900/30 rounded-lg p-3">
             <div className="flex items-center gap-2 text-red-400 mb-2">
                <AlertCircle size={14} />
                <span className="text-xs font-bold uppercase">Friction Points</span>
             </div>
             <ul className="list-disc list-inside text-xs text-red-300/80 space-y-1">
                {problems.map((p, i) => <li key={i}>{p}</li>)}
             </ul>
          </div>
        </div>

        {/* Center: Arrow Transition */}
        <div className="hidden md:flex flex-col items-center justify-center text-slate-600">
           <motion.div 
             animate={{ x: [0, 5, 0], opacity: [0.5, 1, 0.5] }} 
             transition={{ repeat: Infinity, duration: 2 }}
           >
             <ArrowRight size={32} />
           </motion.div>
        </div>

        {/* Right: Target State */}
        <div>
           <h3 className="text-xs uppercase tracking-wider text-indigo-400 font-bold mb-2 border-b border-slate-700 pb-2">
            Target: Unified
          </h3>
          
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="bg-gradient-to-br from-slate-800 to-indigo-950/30 rounded-xl border border-indigo-500/30 p-5 shadow-xl relative overflow-hidden"
          >
             <div className="absolute -top-4 -right-4 text-indigo-500/10">
                <Brain size={120} />
             </div>
             
             <div className="relative z-10">
                <div className="flex items-center gap-3 mb-4">
                   <div className="p-2 bg-indigo-600 rounded-lg shadow-lg shadow-indigo-900/50">
                      <Brain size={20} className="text-white" />
                   </div>
                   <div>
                       <div className="text-xs text-indigo-300 uppercase tracking-wide">Unified Model</div>
                       <div className="text-base font-bold text-white leading-tight">{target_state.model}</div>
                   </div>
                </div>
                
                <div className="space-y-3">
                   <div className="bg-slate-900/40 rounded p-2 border border-slate-700/50">
                      <div className="flex items-center gap-2 text-indigo-300 text-[10px] font-bold mb-1.5 uppercase">
                         <Settings size={10} />
                         Personalization
                      </div>
                      <div className="flex gap-1.5 flex-wrap">
                         {(target_state.personalization || []).map(p => (
                            <span key={p} className="text-[10px] bg-indigo-500/20 text-indigo-200 px-2 py-0.5 rounded-full border border-indigo-500/20">
                               {p}
                            </span>
                         ))}
                      </div>
                   </div>

                   <div className="bg-slate-900/40 rounded p-2 border border-slate-700/50">
                       <div className="flex items-center gap-2 text-indigo-300 text-[10px] font-bold mb-1.5 uppercase">
                         <Database size={10} />
                         Data Owner
                      </div>
                      <div className="text-xs text-slate-300 pl-1">
                         {target_state.data_owner}
                      </div>
                   </div>
                </div>
             </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
"""

def main():
    with open(mdx_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    parts = re.split(r'\{\/\*\s*Slide\s+\d+\s*\*\/\}\n?', content)
    
    header = parts[0]
    slides_content = parts[1:] if len(parts) > 1 else []
    
    theme = "business"
    
    slides = []
    for i, slide_mdx in enumerate(slides_content):
        slides.append({
            "mdx": slide_mdx.strip(),
            "slideNumber": i + 1
        })
        
    generated_components = {
        "SurfaceClusterMap": {
            "name": "SurfaceClusterMap",
            "code": surface_cluster_map_code
        },
        "PotteryPromptScene": {
            "name": "PotteryPromptScene",
            "code": create_mock_component("PotteryPromptScene")
        },
        "SurfingEvalScene": {
            "name": "SurfingEvalScene",
            "code": create_mock_component("SurfingEvalScene")
        }
    }
    
    state = {
        "project": "react-mdx",
        "active_theme": theme,
        "slides": slides,
        "generated_components": generated_components
    }
    
    os.makedirs(output_dir, exist_ok=True)
    with open(output_state, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        
    print(f"Created state.json at {output_state}")
    print(f"Number of slides: {len(slides)}")

if __name__ == "__main__":
    main()
