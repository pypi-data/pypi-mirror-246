import { s as styleTags, f as foldNodeProp, c as foldInside, p as parseMixed, t as tags, S as StreamLanguage } from './Index-7ba5d9c9.js';
import { yaml } from './yaml-c63fc23d.js';
import './index-0b565b60.js';
import './svelte/svelte.js';
import './Button-d6e4788d.js';
import './Index-e541bea9.js';
import './Check-f7edb5d9.js';
import './Copy-a69620a8.js';
import './Download-ea83bae3.js';
import './DownloadLink-3ebea447.js';
import './file-url-45e62f9f.js';
import './BlockLabel-f63facf2.js';
import './Empty-fb6b0260.js';
import './Example-ef3222e9.js';

const frontMatterFence = /^---\s*$/m;
const frontmatter = {
  defineNodes: [{ name: "Frontmatter", block: true }, "FrontmatterMark"],
  props: [
    styleTags({
      Frontmatter: [tags.documentMeta, tags.monospace],
      FrontmatterMark: tags.processingInstruction
    }),
    foldNodeProp.add({
      Frontmatter: foldInside,
      FrontmatterMark: () => null
    })
  ],
  wrap: parseMixed((node) => {
    const { parser } = StreamLanguage.define(yaml);
    if (node.type.name === "Frontmatter") {
      return {
        parser,
        overlay: [{ from: node.from + 4, to: node.to - 4 }]
      };
    }
    return null;
  }),
  parseBlock: [
    {
      name: "Frontmatter",
      before: "HorizontalRule",
      parse: (cx, line) => {
        let end = void 0;
        const children = new Array();
        if (cx.lineStart === 0 && frontMatterFence.test(line.text)) {
          children.push(cx.elt("FrontmatterMark", 0, 4));
          while (cx.nextLine()) {
            if (frontMatterFence.test(line.text)) {
              end = cx.lineStart + 4;
              break;
            }
          }
          if (end !== void 0) {
            children.push(cx.elt("FrontmatterMark", end - 4, end));
            cx.addElement(cx.elt("Frontmatter", 0, end, children));
          }
          return true;
        }
        return false;
      }
    }
  ]
};

export { frontmatter };
//# sourceMappingURL=frontmatter-8fc595f6.js.map
