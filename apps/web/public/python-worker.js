/* The original repository's browser Python runtime, isolated from the UI thread. */
importScripts('/runtime/skulpt.min.js', '/runtime/skulpt-stdlib.js');
self.onmessage = async ({data}) => {
  let output = '';
  Sk.configure({
    output: (text) => { output += text; if (output.length > 100000) throw new Error('Output limit reached (100,000 characters).'); },
    read: (name) => {
      const file = Sk.builtinFiles?.files?.[name];
      if (file === undefined) throw new Error('Module not available in the browser runtime: ' + name);
      return file;
    },
    __future__: Sk.python3,
    execLimit: 10000,
  });
  try {
    await Sk.misceval.asyncToPromise(() => Sk.importMainWithBody('<stdin>', false, data.code, true));
    self.postMessage({output:output || '(completed without printed output)',status:'Completed'});
  } catch(error) {
    self.postMessage({output:output + '\n' + String(error),status:'Error'});
  }
};
