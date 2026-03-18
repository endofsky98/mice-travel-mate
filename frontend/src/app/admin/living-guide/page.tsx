'use client';

import { useEffect, useState } from 'react';
import { Plus, Pencil, Trash2, BookOpen, ChevronRight, ArrowLeft } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Modal from '@/components/ui/Modal';
import Tabs from '@/components/ui/Tabs';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import { LivingGuideCategory, LivingGuideArticle, SUPPORTED_LANGUAGES } from '@/types';

export default function AdminLivingGuidePage() {
  const { lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState<LivingGuideCategory[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<LivingGuideCategory | null>(null);
  const [articles, setArticles] = useState<LivingGuideArticle[]>([]);
  const [loadingArticles, setLoadingArticles] = useState(false);

  // Category modal
  const [showCatModal, setShowCatModal] = useState(false);
  const [editingCat, setEditingCat] = useState<LivingGuideCategory | null>(null);
  const [catFormData, setCatFormData] = useState<Record<string, string>>({});
  const [catFormLangTab, setCatFormLangTab] = useState('en');

  // Article modal
  const [showArtModal, setShowArtModal] = useState(false);
  const [editingArt, setEditingArt] = useState<LivingGuideArticle | null>(null);
  const [artFormData, setArtFormData] = useState<Record<string, string>>({});
  const [artFormLangTab, setArtFormLangTab] = useState('en');

  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchCategories(); }, []);

  const fetchCategories = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: LivingGuideCategory[] }>('/api/admin/living-guide/categories');
      setCategories(data.items || []);
    } catch { setCategories([]); }
    setLoading(false);
  };

  const fetchArticles = async (categoryId: string) => {
    setLoadingArticles(true);
    try {
      const data = await api.get<{ items: LivingGuideArticle[] }>(`/api/admin/living-guide/categories/${categoryId}/articles`);
      setArticles(data.items || []);
    } catch { setArticles([]); }
    setLoadingArticles(false);
  };

  const selectCategory = (cat: LivingGuideCategory) => {
    setSelectedCategory(cat);
    fetchArticles(cat.id);
  };

  // Category CRUD
  const openCreateCatModal = () => {
    setEditingCat(null);
    const data: Record<string, string> = { icon: '' };
    SUPPORTED_LANGUAGES.forEach((l) => { data[`name_${l.code}`] = ''; });
    setCatFormData(data);
    setCatFormLangTab('en');
    setShowCatModal(true);
  };

  const openEditCatModal = (cat: LivingGuideCategory) => {
    setEditingCat(cat);
    const data: Record<string, string> = { icon: cat.icon || '' };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = typeof cat.name === 'object' ? cat.name[l.code] || '' : l.code === 'en' ? (cat.name as string) : '';
    });
    setCatFormData(data);
    setCatFormLangTab('en');
    setShowCatModal(true);
  };

  const handleSaveCat = async () => {
    setSaving(true);
    try {
      const name: Record<string, string> = {};
      SUPPORTED_LANGUAGES.forEach((l) => { if (catFormData[`name_${l.code}`]) name[l.code] = catFormData[`name_${l.code}`]; });
      const payload = { name, icon: catFormData.icon || undefined };
      if (editingCat) {
        await api.put(`/api/admin/living-guide/categories/${editingCat.id}`, payload);
      } else {
        await api.post('/api/admin/living-guide/categories', payload);
      }
      setShowCatModal(false);
      fetchCategories();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDeleteCat = async (id: string) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try {
      await api.delete(`/api/admin/living-guide/categories/${id}`);
      if (selectedCategory?.id === id) { setSelectedCategory(null); setArticles([]); }
      fetchCategories();
    } catch { alert('삭제에 실패했습니다'); }
  };

  // Article CRUD
  const openCreateArtModal = () => {
    setEditingArt(null);
    const data: Record<string, string> = { image_url: '' };
    SUPPORTED_LANGUAGES.forEach((l) => { data[`title_${l.code}`] = ''; data[`content_${l.code}`] = ''; });
    setArtFormData(data);
    setArtFormLangTab('en');
    setShowArtModal(true);
  };

  const openEditArtModal = (art: LivingGuideArticle) => {
    setEditingArt(art);
    const data: Record<string, string> = { image_url: art.image_url || '' };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`title_${l.code}`] = typeof art.title === 'object' ? art.title[l.code] || '' : l.code === 'en' ? (art.title as string) : '';
      data[`content_${l.code}`] = typeof art.content === 'object' ? (art.content?.[l.code] || '') : l.code === 'en' ? ((art.content as string) || '') : '';
    });
    setArtFormData(data);
    setArtFormLangTab('en');
    setShowArtModal(true);
  };

  const handleSaveArt = async () => {
    if (!selectedCategory) return;
    setSaving(true);
    try {
      const title: Record<string, string> = {};
      const content: Record<string, string> = {};
      SUPPORTED_LANGUAGES.forEach((l) => {
        if (artFormData[`title_${l.code}`]) title[l.code] = artFormData[`title_${l.code}`];
        if (artFormData[`content_${l.code}`]) content[l.code] = artFormData[`content_${l.code}`];
      });
      const payload = { title, content, image_url: artFormData.image_url || undefined, category_id: selectedCategory.id };
      if (editingArt) {
        await api.put(`/api/admin/living-guide/articles/${editingArt.id}`, payload);
      } else {
        await api.post(`/api/admin/living-guide/categories/${selectedCategory.id}/articles`, payload);
      }
      setShowArtModal(false);
      fetchArticles(selectedCategory.id);
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDeleteArt = async (id: string) => {
    if (!selectedCategory || !confirm('정말 삭제하시겠습니까?')) return;
    try { await api.delete(`/api/admin/living-guide/articles/${id}`); fetchArticles(selectedCategory.id); } catch { alert('삭제에 실패했습니다'); }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          {selectedCategory && (
            <button onClick={() => { setSelectedCategory(null); setArticles([]); }} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded-lg">
              <ArrowLeft className="w-5 h-5 text-gray-500" />
            </button>
          )}
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {selectedCategory ? `생활 가이드 - ${lt(selectedCategory.name)}` : '생활 가이드 관리'}
          </h1>
        </div>
        {selectedCategory ? (
          <Button onClick={openCreateArtModal}><Plus className="w-4 h-4" />글 추가</Button>
        ) : (
          <Button onClick={openCreateCatModal}><Plus className="w-4 h-4" />카테고리 추가</Button>
        )}
      </div>

      {/* Category List */}
      {!selectedCategory && (
        categories.length === 0 ? (
          <EmptyState icon={BookOpen} title="카테고리가 없습니다" actionLabel="카테고리 추가" onAction={openCreateCatModal} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {categories.map((cat) => (
              <Card key={cat.id} className="p-5 cursor-pointer hover:shadow-md transition-shadow" onClick={() => selectCategory(cat)}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center text-xl">
                      {cat.icon || '📖'}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100">{lt(cat.name)}</h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{cat.articles?.length || 0}개 글</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <button onClick={(e) => { e.stopPropagation(); openEditCatModal(cat); }} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded"><Pencil className="w-4 h-4 text-gray-500" /></button>
                    <button onClick={(e) => { e.stopPropagation(); handleDeleteCat(cat.id); }} className="p-1 hover:bg-red-50 dark:hover:bg-red-950/40 rounded"><Trash2 className="w-4 h-4 text-red-500" /></button>
                    <ChevronRight className="w-4 h-4 text-gray-400 ml-1" />
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )
      )}

      {/* Article List */}
      {selectedCategory && (
        loadingArticles ? <LoadingSpinner fullPage /> : articles.length === 0 ? (
          <EmptyState icon={BookOpen} title="이 카테고리에 글이 없습니다" actionLabel="글 추가" onAction={openCreateArtModal} />
        ) : (
          <Card className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-dark-input">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">제목</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">이미지</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">작업</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                  {articles.map((art) => (
                    <tr key={art.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                      <td className="px-6 py-4 text-sm text-gray-500">{art.id}</td>
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{lt(art.title)}</td>
                      <td className="px-6 py-4">
                        {art.image_url ? (
                          <div className="w-12 h-8 rounded bg-gray-100 dark:bg-gray-800 overflow-hidden">
                            <img src={art.image_url} alt="" className="w-full h-full object-cover" />
                          </div>
                        ) : <span className="text-xs text-gray-400">-</span>}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <button onClick={() => openEditArtModal(art)} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded"><Pencil className="w-4 h-4 text-gray-500" /></button>
                          <button onClick={() => handleDeleteArt(art.id)} className="p-1 hover:bg-red-50 dark:hover:bg-red-950/40 rounded"><Trash2 className="w-4 h-4 text-red-500" /></button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )
      )}

      {/* Category Modal */}
      <Modal isOpen={showCatModal} onClose={() => setShowCatModal(false)} title={editingCat ? '카테고리 수정' : '카테고리 추가'} size="md">
        <div className="space-y-4">
          <Input label="아이콘 (이모지 또는 이름)" value={catFormData.icon || ''} onChange={(e) => setCatFormData((p) => ({ ...p, icon: e.target.value }))} placeholder="예: 📖 또는 book" />
          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">다국어 콘텐츠</p>
            <Tabs tabs={langTabs} activeTab={catFormLangTab} onChange={setCatFormLangTab} className="mb-4" />
            <Input label={`이름 (${catFormLangTab})`} value={catFormData[`name_${catFormLangTab}`] || ''} onChange={(e) => setCatFormData((p) => ({ ...p, [`name_${catFormLangTab}`]: e.target.value }))} />
          </div>
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-500/40">
            <Button variant="outline" onClick={() => setShowCatModal(false)}>취소</Button>
            <Button onClick={handleSaveCat} disabled={saving}>{saving ? '로딩 중...' : '저장'}</Button>
          </div>
        </div>
      </Modal>

      {/* Article Modal */}
      <Modal isOpen={showArtModal} onClose={() => setShowArtModal(false)} title={editingArt ? '글 수정' : '글 추가'} size="lg">
        <div className="space-y-4">
          <Input label="이미지 URL" value={artFormData.image_url || ''} onChange={(e) => setArtFormData((p) => ({ ...p, image_url: e.target.value }))} />
          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">다국어 콘텐츠</p>
            <Tabs tabs={langTabs} activeTab={artFormLangTab} onChange={setArtFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input label={`제목 (${artFormLangTab})`} value={artFormData[`title_${artFormLangTab}`] || ''} onChange={(e) => setArtFormData((p) => ({ ...p, [`title_${artFormLangTab}`]: e.target.value }))} />
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">내용 ({artFormLangTab})</label>
                <textarea
                  className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[160px] resize-y"
                  value={artFormData[`content_${artFormLangTab}`] || ''}
                  onChange={(e) => setArtFormData((p) => ({ ...p, [`content_${artFormLangTab}`]: e.target.value }))}
                />
              </div>
            </div>
          </div>
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-500/40">
            <Button variant="outline" onClick={() => setShowArtModal(false)}>취소</Button>
            <Button onClick={handleSaveArt} disabled={saving}>{saving ? '로딩 중...' : '저장'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
