import android.content.Context
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.kotlinesample.R
import com.example.kotlinesample.entity.Article
import kotlinx.android.synthetic.main.rv_item_article.view.*

class RVArticleAdapter(val context: Context, val items: ArrayList<Article>) : RecyclerView.Adapter<RVArticleAdapter.MainViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, p1: Int) = MainViewHolder(parent)


    override fun getItemCount(): Int = items.size

    override fun onBindViewHolder(holer: MainViewHolder, position: Int) {
        items[position].let { item ->
            with(holer) {
                title.text = item.title
            }
        }
    }

    inner class MainViewHolder(parent: ViewGroup) : RecyclerView.ViewHolder(
        LayoutInflater.from(parent.context).inflate(R.layout.rv_item_article, parent, false)) {
        val title = itemView.tv_article_title
        val preview = itemView.iv_preview
    }
}
