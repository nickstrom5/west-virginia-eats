import SwiftUI
import UIKit
import CoreText

/// West Virginia palette, a landscape one (provisional, 2026-11-05; Nick decides, playbook/05-naming.md), light only. WVU's gold and blue
/// against Marshall's green splits the state, and the 1963 state colors read as WVU, so the colors come from the land
/// (state-prompts/WEST_VIRGINIA_PROMPT.md): ridge green #2E5E3E (7.5:1 on white) for titles, tint and accents; gorge slate #1F3B5C (white
/// on it 11.4:1) for the hand-checked guide cards; rhododendron #C2477A for honors chips (white on it 4.7:1); maple gold #E0A526 only as a
/// pin and card fill under coal #1E1E1E (7.6:1); cream #F6F1E6 pages. The names `green`/`gold` are kept from Wisconsin Eats so the shared
/// views read the same; here `green` is ridge green and `gold` is gorge slate.
enum Theme {
    static let green = Color(hex: 0x2E5E3E)      // ridge green: titles, tint, primary text accents
    static let green2 = Color(hex: 0x3F7A52)
    static let gold = Color(hex: 0x1F3B5C)       // gorge slate: card fills under white text, chips
    static let goldSoft = Color(hex: 0xDCE4EE)   // soft slate
    static let lime = Color(hex: 0xE0A526)       // maple gold, fills only (hand-checked pins, the title shadow), under coal
    static let limeSoft = Color(hex: 0xF8E7BE)
    static let sand = Color(hex: 0xF6F1E6)       // the Home background, cream
    static let red = Color(hex: 0xC2477A)        // rhododendron: honors chips
    static let sandstone = Color(hex: 0xC2477A)  // rhododendron accent (4.7:1 on white)
    static let teal = Color(hex: 0x1F6E78)       // New River accent (5.9:1 on white)
    static let ink = Color(hex: 0x1E1E1E)
    static let ink2 = Color(hex: 0x2E3440)
    static let muted = Color(hex: 0x5B6270)
    static let surface = Color.white
    static let surface2 = Color(hex: 0xF1EEE6)
    static let surface3 = Color(hex: 0xE4DFD3)
    static let rule = Color(hex: 0xE4DFD3)
    static let rule2 = Color(hex: 0xCCC4B3)
}

extension Color {
    init(hex: UInt32) {
        self.init(red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255, blue: Double(hex & 0xFF) / 255)
    }
}

/// A small uppercase label: "STONE CRAB", "1 MICHELIN STAR".
struct Chip: View {
    enum Style { case gold, green, red, plain, dashed }
    let text: String
    var style: Style = .plain

    var body: some View {
        Text(text.uppercased())
            .font(.caption2.weight(.bold))
            .tracking(0.4)
            .padding(.horizontal, 7).padding(.vertical, 3)
            .foregroundStyle(style == .green || style == .red ? Color.white : style == .dashed ? Theme.muted : style == .gold ? Theme.ink : Theme.green)
            .background {
                RoundedRectangle(cornerRadius: 5).fill(style == .gold ? Theme.goldSoft : style == .green ? Theme.green : style == .red ? Theme.red
                                                       : style == .dashed ? .clear : Theme.surface2)
            }
            .overlay {
                if style == .dashed { RoundedRectangle(cornerRadius: 5).strokeBorder(Theme.rule2, style: StrokeStyle(lineWidth: 1, dash: [3, 2])) }
            }
            .accessibilityLabel(text)
    }
}

/// West Virginia Eats' lettering: the system face drawn compressed and heavy for titles and guide names (like a show poster), and the
/// system monospaced face for numbers, dates and small labels. No bundled fonts.
struct DisplayFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .black
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight).width(.compressed))
    }
}

/// Numbers, dates and small labels in the system monospaced face, scaled like DisplayFont.
struct MonoFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .semibold
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight, design: .monospaced))
    }
}

extension View {
    func displayFont(_ size: CGFloat, weight: Font.Weight = .black) -> some View {
        modifier(DisplayFont(size: size, weight: weight))
    }

    func monoFont(_ size: CGFloat, weight: Font.Weight = .semibold) -> some View {
        modifier(MonoFont(size: size, weight: weight))
    }
}

/// The header band: layered Allegheny ridgelines fading from slate at the back to ridge green in front, over a maple-gold baseline.
struct Stripes: View {
    var height: CGFloat = 6

    /// (x, rise) for each ridge, back to front: 0 is the baseline, 1 the band's top
    static let ridges: [[(CGFloat, CGFloat)]] = [
        [(0, 0.82), (0.10, 0.95), (0.22, 0.80), (0.35, 1.0), (0.50, 0.84), (0.63, 0.97), (0.78, 0.82), (0.90, 0.94), (1, 0.86)],
        [(0, 0.55), (0.14, 0.70), (0.28, 0.56), (0.42, 0.74), (0.58, 0.58), (0.72, 0.72), (0.88, 0.56), (1, 0.64)],
        [(0, 0.28), (0.16, 0.42), (0.32, 0.30), (0.50, 0.46), (0.66, 0.32), (0.82, 0.44), (1, 0.30)]]

    var body: some View {
        Canvas { ctx, size in
            let w = size.width, h = size.height, base = h * 0.78
            for (i, ridge) in Self.ridges.enumerated() {
                var p = Path()
                p.move(to: CGPoint(x: 0, y: base))
                for (x, rise) in ridge { p.addLine(to: CGPoint(x: x * w, y: base - base * rise)) }
                p.addLine(to: CGPoint(x: w, y: base)); p.closeSubpath()
                ctx.fill(p, with: .color([Theme.gold.opacity(0.55), Theme.gold, Theme.green][i]))
            }
            // the maple-gold baseline last
            ctx.fill(Path(CGRect(x: 0, y: base, width: w, height: h - base)), with: .color(Theme.lime))
        }
        .frame(height: height * 2.4)
        .clipShape(RoundedRectangle(cornerRadius: 3))
        .accessibilityHidden(true)
    }
}

extension View {
    /// An inline navigation title in the display type. UINavigationBar.appearance() didn't reach every SwiftUI bar on iOS 27
    /// (the Map title went from compressed blue to plain black after a push and pop; place titles were always plain), so the
    /// title is our own view in the bar. The navigation title is still set, for the back button and VoiceOver.
    func inlineTitle(_ title: String) -> some View {
        navigationTitle(title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text(title).displayFont(19, weight: .heavy).foregroundStyle(Theme.green)
                        .lineLimit(1).minimumScaleFactor(0.7)
                        .accessibilityAddTraits(.isHeader)
                }
            }
    }
}
