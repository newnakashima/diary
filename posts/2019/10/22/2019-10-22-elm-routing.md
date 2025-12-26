---
templateKey: blog-post
title:  "Elm初心者がURLルーティングを頑張ってみた結果"
date:   2019-10-22 22:14:00 +0900
categories: Elm
---

Elmで複数のページがあるSPA的なのを作りたいと思って公式のチュートリアルを読んでみた。

[https://guide.elm-lang.org/webapps/url_parsing.html](https://guide.elm-lang.org/webapps/url_parsing.html)

パーサーの作り方は載っているのだが、肝心の使い方については、「TODO」の悲しい４文字。。。

色々やってみて、ページを遷移させることについてはなんとか成功したので備忘録として残しておく。

## 元となるファイル

[https://guide.elm-lang.org/webapps/navigation.html](https://guide.elm-lang.org/webapps/navigation.html)

上記のページに載っているソースコードを元に改造する。

```elm
import Browser
import Browser.Navigation as Nav
import Html exposing (..)
import Html.Attributes exposing (..)
import Url



-- MAIN


main : Program () Model Msg
main =
  Browser.application
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    , onUrlChange = UrlChanged
    , onUrlRequest = LinkClicked
    }



-- MODEL


type alias Model =
  { key : Nav.Key
  , url : Url.Url
  }


init : () -> Url.Url -> Nav.Key -> ( Model, Cmd Msg )
init flags url key =
  ( Model key url, Cmd.none )



-- UPDATE


type Msg
  = LinkClicked Browser.UrlRequest
  | UrlChanged Url.Url


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    LinkClicked urlRequest ->
      case urlRequest of
        Browser.Internal url ->
          ( model, Nav.pushUrl model.key (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )

    UrlChanged url ->
      ( { model | url = url }
      , Cmd.none
      )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
  Sub.none



-- VIEW


view : Model -> Browser.Document Msg
view model =
  { title = "URL Interceptor"
  , body =
      [ text "The current URL is: "
      , b [] [ text (Url.toString model.url) ]
      , ul []
          [ viewLink "/home"
          , viewLink "/profile"
          , viewLink "/reviews/the-century-of-the-self"
          , viewLink "/reviews/public-opinion"
          , viewLink "/reviews/shah-of-shahs"
          ]
      ]
  }


viewLink : String -> Html msg
viewLink path =
  li [] [ a [ href path ] [ text path ] ]
```

このコードでも、なんとなくブラウザのURLバーのURLは変わってるしHTMLのテキストも変わってるのはわかる。でもURLによって表示するコンテンツをまるごと切り替える、みたいなのはできない。

そこで、さっきもはったURLパースのやり方を書いてるページを参考にコードに書き足していく。

[https://guide.elm-lang.org/webapps/url_parsing.html](https://guide.elm-lang.org/webapps/url_parsing.html)

URLを見る限り、ホーム、プロフィール、レビューの三種類があるようだ。

```elm
-- import 文を追加する

import Url.Parser exposing (Parser, parse, (</>), map, oneOf, s, string, top)

-- 中略

type Route
  = Home
  | Profile
  | Reviews String

-- 中略

routeParser : Parser (Route -> a) a
routeParser =
  oneOf
    [ map Home top
    , map Profile (s "profile")
    , map Reviews (s "reviews" </> string)
    ]
```

公式のチュートリアルに書いてあるのはここまでだけど、実際にURLをパースするには下記のような関数を書く。

参考: [https://package.elm-lang.org/packages/elm/url/latest/Url-Parser#parse](https://package.elm-lang.org/packages/elm/url/latest/Url-Parser#parse)

```elm
toRoute : String -> Route
toRoute string =
  case Url.fromString string of
    Nothing ->
      Home
    Just url ->
      Maybe.withDefault Home (parse routeParser url)
```

さらに、現在の状態をmodelで保持できるようにする。

```elm
type Page
  = HomePage
  | ProfilePage
  | ReviewsPage String

type alias Model =
  { key : Nav.Key
  , url : Url.Url
  , page : Page
  }

init : () -> Url.Url -> Nav.Key -> ( Model, Cmd Msg )
init flags url key =
  ( Model key url HomePage, Cmd.none )
```

そしてURLが更新されたタイミングでURLをパースするようにupdateを修正。

```elm
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    LinkClicked urlRequest ->
      case urlRequest of
        Browser.Internal url ->
          case toRoute (Url.toString url) of
            Home ->
              ( { model | page = HomePage }, Nav.pushUrl model.key (Url.toString url) )
            Profile ->
              ( { model | page = ProfilePage }, Nav.pushUrl model.key (Url.toString url) )
            Reviews name ->
              ( { model | page = ReviewsPage name }, Nav.pushUrl model.key (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )

    UrlChanged url ->
      case toRoute (Url.toString url) of
        Home ->
          ( { model | url = url, page = HomePage }
          , Cmd.none
          )
        Profile ->
          ( { model | url = url, page = ProfilePage }
          , Cmd.none
          )
        Reviews name ->
          ( { model | url = url, page = ReviewsPage name }
          , Cmd.none
          )
```

あとはページの種類によって内容を切り替える。

```elm
view : Model -> Browser.Document Msg
view model =
  { title = "URL Interceptor"
  , body =
      [ text "The current URL is: "
      , b [] [ text (Url.toString model.url) ]
      , case model.page of
          HomePage -> ul []
            [ viewLink "/home"
            , viewLink "/profile"
            , viewLink "/reviews/the-century-of-the-self"
            , viewLink "/reviews/public-opinion"
            , viewLink "/reviews/shah-of-shahs"
            ]
          ProfilePage -> p [] [ text "profile page" ]
          ReviewsPage name -> p [] [ text (name ++ "'s review page.") ]
      ]
  }
```

これで一応URLをパースして表示内容を切り替えることはできるようになった。

多分というか絶対もっといい書き方があると思うが、それはこれからの修行だ。。。

最終的なソースは下記のようになった。

```elm
import Browser
import Browser.Navigation as Nav
import Html exposing (..)
import Html.Attributes exposing (..)
import Url
import Url.Parser exposing (Parser, parse, (</>), map, oneOf, s, string, top)


-- MAIN


main : Program () Model Msg
main =
  Browser.application
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    , onUrlChange = UrlChanged
    , onUrlRequest = LinkClicked
    }


-- URL Routing

type Route
  = Home
  | Profile
  | Reviews String

routeParser : Parser (Route -> a) a
routeParser =
  oneOf
  [ map Home top
  , map Profile (s "profile")
  , map Reviews (s "reviews" </> string)
  ]

toRoute : String -> Route
toRoute string =
  case Url.fromString string of
    Nothing ->
      Home
    Just url ->
      Maybe.withDefault Home (parse routeParser url)

-- MODEL

type Page
  = HomePage
  | ProfilePage
  | ReviewsPage String

type alias Model =
  { key : Nav.Key
  , url : Url.Url
  , page : Page
  }


init : () -> Url.Url -> Nav.Key -> ( Model, Cmd Msg )
init flags url key =
  ( Model key url HomePage, Cmd.none )



-- UPDATE


type Msg
  = LinkClicked Browser.UrlRequest
  | UrlChanged Url.Url


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    LinkClicked urlRequest ->
      case urlRequest of
        Browser.Internal url ->
          case toRoute (Url.toString url) of
            Home -> 
              ( { model | page = HomePage }, Nav.pushUrl model.key (Url.toString url) )
            Profile ->
              ( { model | page = ProfilePage }, Nav.pushUrl model.key (Url.toString url) )
            Reviews name ->
              ( { model | page = ReviewsPage name }, Nav.pushUrl model.key (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )

    UrlChanged url ->
      case toRoute (Url.toString url) of
        Home ->
          ( { model | url = url, page = HomePage }
          , Cmd.none
          )
        Profile ->
          ( { model | url = url, page = ProfilePage }
          , Cmd.none
          )
        Reviews name ->
          ( { model | url = url, page = ReviewsPage name }
          , Cmd.none
          )
          



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
  Sub.none



-- VIEW


view : Model -> Browser.Document Msg
view model =
  { title = "URL Interceptor"
  , body =
      [ text "The current URL is: "
      , b [] [ text (Url.toString model.url) ]
      , case model.page of
          HomePage -> ul []
            [ viewLink "/home"
            , viewLink "/profile"
            , viewLink "/reviews/the-century-of-the-self"
            , viewLink "/reviews/public-opinion"
            , viewLink "/reviews/shah-of-shahs"
            ]
          ProfilePage -> p [] [ text "profile page" ]
          ReviewsPage name -> p [] [ text (name ++ "'s review page.") ]
      ]
  }


viewLink : String -> Html msg
viewLink path =
  li [] [ a [ href path ] [ text path ] ]
```

モジュールへの分割などをこれから勉強したい。

