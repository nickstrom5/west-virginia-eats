import Foundation
import CoreLocation
import UIKit

/// `-screenshot <name>` opens one screen with fixed state for App Store screenshots (scripts/capture-screenshots.sh).
/// Names: home, rolls, dogs, italian, ramps, farm, inns, fish, honors, oldest, detail, map, saved, about.
enum ScreenshotMode {
    /// Debug builds only: an App Store build ignores the launch argument, so no one can reach seeded screens or fake locations.
    static var name: String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: "-screenshot"), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
    static var isActive: Bool { name != nil }

    @MainActor
    static func apply(to model: AppModel) {
        guard let name, model.isLoaded else { return }
        model.filters = Filters()
        // downtown Charleston (the Capitol), so "nearest" lists have distances without a permission prompt
        model.screenshotLocation = CLLocation(latitude: 38.3498, longitude: -81.6326)
        // by name and town, ignoring case, so a rebuild with a slightly different casing still finds the place; the hand-checked one first
        let pick = { (n: String, town: String?) -> Place? in
            let hits = model.places.filter { $0.name.caseInsensitiveCompare(n) == .orderedSame && (town == nil || $0.city == town) }
            return hits.first(where: \.handChecked) ?? hits.first
        }
        for p in [pick("Country Club Bakery", "Fairmont"), pick("Jim's Steak and Spaghetti House", "Huntington"), pick("Morrison's Drive Inn", "Logan")]
            .compactMap({ $0 }) where !model.isSaved(p) {
            model.toggleSaved(p)
        }
        let open = { (g: Guide) in model.tab = .guides; model.selectedGuide = g; model.guidesPath = [.guide(g)] }
        switch name {
        case "rolls", "italian":
            // Fairmont, between the Fairmont and Clarksburg bakeries and Italian kitchens
            model.screenshotLocation = CLLocation(latitude: 39.4851, longitude: -80.1426)
            open(name == "rolls" ? .rolls : .italian)
        case "dogs": open(.dogs)
        case "ramps": open(.ramps)
        case "farm": open(.farm)
        case "inns": open(.inns)
        case "fish": open(.fish)
        case "honors": open(.honors)
        case "oldest": open(.oldest)
        case "detail":
            // Jim's Steak and Spaghetti House: an Italian classic and a James Beard America's Classic, with its note
            open(.italian)
            if let p = pick("Jim's Steak and Spaghetti House", "Huntington") ?? model.places.first {
                model.selectedPlace = p; model.guidesPath.append(.place(p))
            }
        case "map": model.tab = .map
        case "saved": model.tab = .saved
        case "about": model.tab = .about
        default: model.tab = .guides; model.selectedGuide = nil
        }
        // iPad shows the place column next to every list, so give each shot a place instead of "Pick a place": a different
        // honored or hand-checked one per shot.
        guard UIDevice.current.userInterfaceIdiom == .pad, model.selectedPlace == nil else { return }
        let place: Place? = switch name {
        case "home": pick("Country Club Bakery", "Fairmont")
        case "rolls": pick("Country Club Bakery", "Fairmont")
        case "dogs": pick("Morrison's Drive Inn", "Logan")
        case "italian": pick("Minard's Spaghetti Inn", "Clarksburg")
        case "ramps": pick("Mack's Bingo Kitchen", "Wardensville")
        case "farm": pick("1010 Bridge Restaurant", "Charleston")
        case "map": pick("1010 Bridge Restaurant", "Charleston")
        case "honors": pick("Figaretti's Restaurant", "Wheeling")
        case "oldest": pick("North End Tavern & Brewery", "Parkersburg")
        case "saved": pick("Country Club Bakery", "Fairmont")
        case "about": nil
        default: pick("Jim's Steak and Spaghetti House", "Huntington")
        }
        model.selectedPlace = place
    }
}
