
Action: file_editor view /app/frontend/src/App.css
Observation: /app/frontend/src/App.css:
1|@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@100;200;300;400;500;600;700;800;900&display=swap');
2|
3|* {
4|  margin: 0;
5|  padding: 0;
6|  box-sizing: border-box;
7|}
8|
9|body {
10|  font-family: 'Exo 2', sans-serif;
11|  background: #000;
12|  color: #fff;
13|  overflow-x: hidden;
14|}
15|
16|.App {
17|  min-height: 100vh;
18|}
19|
20|/* Custom scrollbar */
21|::-webkit-scrollbar {
22|  width: 8px;
23|}
24|
25|::-webkit-scrollbar-track {
26|  background: #1a1a1a;
27|}
28|
29|::-webkit-scrollbar-thumb {
30|  background: linear-gradient(to bottom, #ef4444, #f97316);
31|  border-radius: 4px;
32|}
33|
34|::-webkit-scrollbar-thumb:hover {
35|  background: linear-gradient(to bottom, #dc2626, #ea580c);
36|}
37|
38|/* Animations */
39|@keyframes fadeIn {
40|  from {
41|    opacity: 0;
42|    transform: translateY(20px);
43|  }
44|  to {
45|    opacity: 1;
46|    transform: translateY(0);
47|  }
48|}
49|
50|@keyframes slideUp {
51|  from {
52|    transform: translateY(100px);
53|    opacity: 0;
54|  }
55|  to {
56|    transform: translateY(0);
57|    opacity: 1;
58|  }
59|}
60|
61|@keyframes pulseGlow {
62|  0%, 100% {
63|    box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
64|  }
65|  50% {
66|    box-shadow: 0 0 40px rgba(239, 68, 68, 0.8), 0 0 60px rgba(249, 115, 22, 0.4);
67|  }
68|}
69|
70|/* Utility Classes */
71|.animate-fadeIn {
72|  animation: fadeIn 0.6s ease-out;
73|}
74|
75|.animate-slideUp {
76|  animation: slideUp 0.8s ease-out;
77|}
78|
79|.animate-pulseGlow {
80|  animation: pulseGlow 2s infinite;
81|}
82|
83|/* Button Styles */
84|button {
85|  cursor: pointer;
86|  transition: all 0.3s ease;
87|}
88|
89|button:hover {
90|  transform: translateY(-2px);
91|}
92|
93|button:active {
94|  transform: translateY(0);
95|}
96|
97|/* Form Elements */
98|input, textarea, select {
99|  transition: all 0.3s ease;
100|}
101|
102|input:focus, textarea:focus, select:focus {
103|  transform: translateY(-1px);
104|  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
105|}
106|
107|/* Card Hover Effects */
108|.card-hover {
109|  transition: all 0.3s ease;
110|  position: relative;
111|  overflow: hidden;
112|}
113|
114|.card-hover::before {
115|  content: '';
116|  position: absolute;
117|  top: 0;
118|  left: -100%;
119|  width: 100%;
120|  height: 100%;
121|  background: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.1), transparent);
122|  transition: left 0.5s;
123|}
124|
125|.card-hover:hover::before {
126|  left: 100%;
127|}
128|
129|.card-hover:hover {
130|  transform: translateY(-4px);
131|  box-shadow: 0 8px 40px rgba(239, 68, 68, 0.2);
132|}
133|
134|/* Image Effects */
135|.img-hover {
136|  transition: all 0.5s ease;
137|  overflow: hidden;
138|}
139|
140|.img-hover img {
141|  transition: transform 0.5s ease;
142|}
143|
144|.img-hover:hover img {
145|  transform: scale(1.1);
146|}
147|
148|/* Text Selection */
149|::selection {
150|  background: rgba(239, 68, 68, 0.3);
151|  color: white;
152|}
153|
154|/* Loading States */
155|.loading-shimmer {
156|  background: linear-gradient(90deg, #374151 25%, #4b5563 50%, #374151 75%);
157|  background-size: 200% 100%;
158|  animation: shimmer 2s infinite;
159|}
160|
161|@keyframes shimmer {
162|  0% {
163|    background-position: -200% 0;
164|  }
165|  100% {
166|    background-position: 200% 0;
167|  }
168|}
169|
170|/* Typography */
171|h1, h2, h3, h4, h5, h6 {
172|  font-weight: 800;
173|  letter-spacing: -0.025em;
174|}
175|
176|.text-gradient {
177|  background: linear-gradient(135deg, #ef4444, #f97316);
178|  background-clip: text;
179|  -webkit-background-clip: text;
180|  -webkit-text-fill-color: transparent;
181|}
182|
183|/* Backdrop Blur Support */
184|.backdrop-blur-fallback {
185|  background: rgba(0, 0, 0, 0.8);
186|}
187|
188|@supports (backdrop-filter: blur(12px)) {
189|  .backdrop-blur-fallback {
190|    backdrop-filter: blur(12px);
191|    background: rgba(0, 0, 0, 0.6);
192|  }
193|}
194|
195|/* Mobile Optimizations */
196|@media (max-width: 768px) {
197|  body {
198|    font-size: 14px;
199|  }
200|  
201|  h1 {
202|    font-size: 2.5rem !important;
203|  }
204|  
205|  h2 {
206|    font-size: 2rem !important;
207|  }
208|  
209|  .mobile-padding {
210|    padding-left: 1rem;
211|    padding-right: 1rem;
212|  }
213|}
214|
215|/* High contrast mode */
216|@media (prefers-contrast: high) {
217|  .bg-gray-800 {
218|    background-color: #000 !important;
219|    border: 2px solid #fff !important;
220|  }
221|  
222|  .text-gray-300 {
223|    color: #fff !important;
224|  }
225|}
226|
227|/* Reduced motion */
228|@media (prefers-reduced-motion: reduce) {
229|  *, *::before, *::after {
230|    animation-duration: 0.01ms !important;
231|    animation-iteration-count: 1 !important;
232|    transition-duration: 0.01ms !important;
233|  }
234|}
235|
236|/* Dark mode enhancements */
237|.dark-mode-shadow {
238|  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(239, 68, 68, 0.1);
239|}
240|
241|/* Performance optimizations */
242|.gpu-accelerated {
243|  transform: translateZ(0);
244|  will-change: transform;
245|}
246|
247|/* Print styles */
248|@media print {
249|  .no-print {
250|    display: none !important;
251|  }
252|  
253|  body {
254|    color: #000 !important;
255|    background: #fff !important;
256|  }
257|}
