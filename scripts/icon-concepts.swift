// West Virginia Eats icon concepts (2026-11-05), drawn in the shared Eats Ranked style (state-prompts/ICON-STYLE.md): one flat, level,
// centred food on ridge green #2E5E3E (the prompt's landscape palette), no backing shape, no text or texture; no flying WV, no Marshall
// "M", no coonskin cap or rifle. Food hexes: roll gold #D9A35B, crumb #F2DDB0, pepperoni #B23A2E, hot dog #A2412C, chili #6E2216,
// slaw #F4F1E6, ramp leaf #7DB35F, ramp stem #8E2F45.
//   A  a pepperoni roll broken open: the golden roll, its cut face dotted with pepperoni
//   B  a slaw dog: a bun, the dog, a band of chili and white slaw on top, side view
//   C  a bunch of ramps: three leaves on burgundy stems with white bulbs, upright
// Usage, from wv-eats/: swift scripts/icon-concepts.swift <out dir>   -> concept-{a,b,c}-1024.png
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let GREEN: UInt32 = 0x2E5E3E, ROLL: UInt32 = 0xD9A35B, CRUMB: UInt32 = 0xF2DDB0, PEP: UInt32 = 0xB23A2E, DOG: UInt32 = 0xA2412C
let CHILI: UInt32 = 0x6E2216, SLAW: UInt32 = 0xF4F1E6, LEAF: UInt32 = 0x7DB35F, STEM: UInt32 = 0x8E2F45

/// A: the pepperoni roll. CoreGraphics y-up, s = canvas size. Identical to make-brand.swift's roll().
func roll(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(ROLL)); c.fillEllipse(in: CGRect(x: 0.15 * s, y: 0.31 * s, width: 0.62 * s, height: 0.38 * s))   // the roll
    c.setFillColor(rgb(CRUMB)); c.fillEllipse(in: CGRect(x: 0.58 * s, y: 0.33 * s, width: 0.27 * s, height: 0.34 * s))  // its broken face
    c.setFillColor(rgb(PEP))
    for (x, y) in [(0.66, 0.53), (0.75, 0.46), (0.67, 0.40), (0.76, 0.57)] {
        c.fillEllipse(in: CGRect(x: CGFloat(x) * s, y: CGFloat(y) * s, width: 0.07 * s, height: 0.07 * s))
    }
}

/// B: a slaw dog: bun, dog, chili, slaw.
func slawdog(_ c: CGContext, _ s: CGFloat) {
    func R(_ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat, _ r: CGFloat) -> CGPath {
        CGPath(roundedRect: CGRect(x: x * s, y: y * s, width: w * s, height: h * s), cornerWidth: r * s, cornerHeight: r * s, transform: nil)
    }
    c.setFillColor(rgb(ROLL)); c.addPath(R(0.16, 0.32, 0.68, 0.20, 0.09)); c.fillPath()
    c.setFillColor(rgb(DOG)); c.addPath(R(0.14, 0.46, 0.72, 0.10, 0.05)); c.fillPath()
    c.setFillColor(rgb(CHILI)); c.addPath(R(0.20, 0.53, 0.60, 0.07, 0.03)); c.fillPath()
    c.setFillColor(rgb(SLAW)); c.addPath(R(0.24, 0.58, 0.52, 0.10, 0.05)); c.fillPath()
}

/// C: a bunch of ramps: three leaves on burgundy stems with white bulbs.
func ramps(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(LEAF))
    for x in [0.24, 0.41, 0.58] { c.fillEllipse(in: CGRect(x: CGFloat(x) * s, y: 0.40 * s, width: 0.18 * s, height: 0.44 * s)) }
    c.setFillColor(rgb(STEM))
    for x in [0.31, 0.48, 0.65] { c.fill(CGRect(x: CGFloat(x) * s, y: 0.20 * s, width: 0.04 * s, height: 0.24 * s)) }
    c.setFillColor(rgb(SLAW))
    for x in [0.295, 0.465, 0.635] { c.fillEllipse(in: CGRect(x: CGFloat(x) * s, y: 0.12 * s, width: 0.07 * s, height: 0.10 * s)) }
}

func render(_ n: Int, _ path: String, _ draw: (CGContext, CGFloat) -> Void) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(GREEN)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n))
    draw(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "playbook/brand"
render(1024, out + "/concept-a-1024.png", roll)
render(1024, out + "/concept-b-1024.png", slawdog)
render(1024, out + "/concept-c-1024.png", ramps)
