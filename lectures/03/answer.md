# 第3回 解答

## 演習

- 第1回（素の LLM）とエージェントの回答の違い：  
    - 素の LLM は一般的な説明になったが、エージェントは用語集を参照して講座の3レベルを具体的に説明した。
- `--trace` で見えたツール呼び出し（ツール名と引数）：  
    - `search_glossary({'query': 'LoRA'})`
    - `search_glossary({'query': 'QLoRA'})`
- 1つの質問での LLM 呼び出し回数（`requests`）：  
    - `requests=2`
- 追加したツールと、docstring に書いた説明：  
    - 追加したツール：`app/tools.py` の `make_quiz(lecture: int) -> str`
    - docstring に書いた説明：

        ```text
        指定した回の用語から、学習の確認問題を1問作って返す。

「第2回の確認問題を出して」のように、講義内容を復習する問題を求められた
ときに使う。問題と、その用語の答えを JSON 文字列で返す。
        ```

## 宿題

- 取り組んだレベル：基礎  
- やったこと：  
    1. `app/agent.py` の `INSTRUCTIONS` から「必ず `search_glossary` で用語集を確認する」という行を削除し、同じ質問を実行した。  
    2. 元に戻したあと、`app/tools.py` の `search_glossary` の docstring にある「用語を1つだけ入れる」を「用語をまとめて入れる」に変更し、同じ質問を実行した。  
    3. どちらも次のコマンドで、ツール名・引数・`requests` を確認した。  
         `uv run python -m app.agent --trace "LoRA とQLoRAの違いは？"`

- 結果：  
    - `INSTRUCTIONS` を変更した場合：`search_glossary({'query': 'LoRA'})` と `search_glossary({'query': 'QLoRA'})` が呼ばれ、`requests=2` だった。回答は途中で終了した。  
    - docstring を変更した場合：同じく `LoRA` と `QLoRA` が別々に検索され、`requests=2` だった。回答は途中で終了した。  
    - 今回の実行では、2つの変更によるツール呼び出し回数や引数の明確な違いは確認できなかった。

- 気づき・疑問：  
    - `INSTRUCTIONS` はエージェント全体への指示で、docstring は個々のツールを使う判断に影響する説明だと分かった。  
    - docstring を「まとめて入れる」に変えても、モデルが必ず複数の用語を1回で検索するとは限らなかった。  
    - 回答が途中で終了した原因が、指示の変更によるものか、API・モデル側の一時的なエラーによるものか疑問が残った。
