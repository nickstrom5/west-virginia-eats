// West Virginia Eats brand (provisional, 2026-11-05; Nick picks the name, icon and palette): the app icon is concept A of
// scripts/icon-concepts.swift, a pepperoni roll broken open, on ridge green; the shared Eats Ranked icon style, state-prompts/ICON-STYLE.md,
// no backing shape. No flying WV, Marshall "M", seal or coat of arms; no "Almost Heaven" or "Country Roads" lines.
// Usage, from wv-eats/: swift scripts/make-brand.swift   -> WestVirginiaEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png,
// docs/ favicons and touch icons, docs/og.png. scripts/make-site.py draws the same mark as its inline SVG: change both together.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let GREEN: UInt32 = 0x2E5E3E, ROLL: UInt32 = 0xD9A35B, CRUMB: UInt32 = 0xF2DDB0, PEP: UInt32 = 0xB23A2E
let SLATE: UInt32 = 0x1F3B5C, GOLD: UInt32 = 0xE0A526, CREAM: UInt32 = 0xF6F1E6

/// A: the pepperoni roll. CoreGraphics y-up, s = canvas size. Identical to icon-concepts.swift's concept A.
func roll(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(ROLL)); c.fillEllipse(in: CGRect(x: 0.15 * s, y: 0.31 * s, width: 0.62 * s, height: 0.38 * s))   // the roll
    c.setFillColor(rgb(CRUMB)); c.fillEllipse(in: CGRect(x: 0.58 * s, y: 0.33 * s, width: 0.27 * s, height: 0.34 * s))  // its broken face
    c.setFillColor(rgb(PEP))
    for (x, y) in [(0.66, 0.53), (0.75, 0.46), (0.67, 0.40), (0.76, 0.57)] {
        c.fillEllipse(in: CGRect(x: CGFloat(x) * s, y: CGFloat(y) * s, width: 0.07 * s, height: 0.07 * s))
    }
}


func render(_ n: Int, _ path: String, background: Bool) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: background ? CGImageAlphaInfo.noneSkipLast.rawValue : CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.setShouldAntialias(true)
    if background { ctx.setFillColor(rgb(GREEN)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n)) }
    roll(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
render(1024, "WestVirginiaEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png", background: true)
try? FileManager.default.createDirectory(atPath: "docs", withIntermediateDirectories: true)
for (n, name) in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")] {
    render(n, "docs/" + name, background: true)
}

/// The share image (1200 x 630): ridge green, the roll at the left, the name and tagline at the right, and the app's header band along
/// the bottom: layered Allegheny ridgelines, slate to green, over a maple-gold baseline, on cream (Theme.swift's Stripes.ridges).
func og(_ path: String) {
    let W = 1200, H = 630
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(GREEN)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    let band: CGFloat = 70, base: CGFloat = 14
    ctx.setFillColor(rgb(CREAM)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: Int(band)))
    let ridges: [[(CGFloat, CGFloat)]] = [
        [(0, 0.82), (0.10, 0.95), (0.22, 0.80), (0.35, 1.0), (0.50, 0.84), (0.63, 0.97), (0.78, 0.82), (0.90, 0.94), (1, 0.86)],
        [(0, 0.55), (0.14, 0.70), (0.28, 0.56), (0.42, 0.74), (0.58, 0.58), (0.72, 0.72), (0.88, 0.56), (1, 0.64)],
        [(0, 0.28), (0.16, 0.42), (0.32, 0.30), (0.50, 0.46), (0.66, 0.32), (0.82, 0.44), (1, 0.30)]]
    let fills = [rgb(SLATE).copy(alpha: 0.55)!, rgb(SLATE), rgb(0x3F7A52)]
    for (i, ridge) in ridges.enumerated() {
        let p = CGMutablePath(); p.move(to: CGPoint(x: 0, y: base))
        for (x, rise) in ridge { p.addLine(to: CGPoint(x: x * CGFloat(W), y: base + (band - base) * rise)) }
        p.addLine(to: CGPoint(x: CGFloat(W), y: base)); p.closeSubpath()
        ctx.setFillColor(fills[i]); ctx.addPath(p); ctx.fillPath()
    }
    ctx.setFillColor(rgb(GOLD)); ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(W), height: base))
    ctx.saveGState(); ctx.translateBy(x: 30, y: 90); roll(ctx, 500); ctx.restoreGState()
    let ns = NSGraphicsContext(cgContext: ctx, flipped: false)
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ns
    let title = NSFont(name: "AvenirNextCondensed-Heavy", size: 80) ?? NSFont.boldSystemFont(ofSize: 70)
    let sub = NSFont(name: "AvenirNextCondensed-DemiBold", size: 34) ?? NSFont.boldSystemFont(ofSize: 30)
    NSAttributedString(string: "WEST VIRGINIA", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 560, y: 380))
    NSAttributedString(string: "EATS", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 560, y: 296))
    NSAttributedString(string: "PEPPERONI ROLLS, HOT DOGS & RAMPS", attributes: [.font: sub, .foregroundColor: NSColor(srgbRed: 0.878, green: 0.647, blue: 0.149, alpha: 1)]).draw(at: NSPoint(x: 564, y: 246))
    NSGraphicsContext.restoreGraphicsState()
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
og("docs/og.png")
