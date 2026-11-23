bool __fastcall sub_143BCC030(__int64 a1, __int64 a2, _WORD *a3, _WORD *a4, char a5)
{
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rax

  if ( a2 != 0 )
  {
    v9 = *(int *)(*(_QWORD *)(a1 + 8) + 4LL);
    v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(a1 + v9 + 8) + 656LL))(a1 + v9 + 8);
    if ( v10 == 0 || *(_BYTE *)(v10 + 47) != 0 || *(_QWORD *)(v10 + 48) == 0 )
      goto LABEL_8;
    v11 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
    v12 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v11 + 656LL))(v11);
    v13 = 0;
    if ( *(_BYTE *)(v12 + 47) == 0 )
      v13 = *(_QWORD *)(v12 + 48);
    v14 = sub_1411E6040(v13, 0, 0);
    if ( v14 == 0 )
LABEL_8:
      v14 = sub_140F75250();
    (*(void (__fastcall **)(__int64, __int64, __int64, _WORD *, _WORD *, char, __int64))(*(_QWORD *)qword_141B5EC88
                                                                                       + 272LL))(
      qword_141B5EC88,
      v14,
      a2,
      a3,
      a4,
      a5,
      a1);
  }
  else
  {
    *a3 = -1;
    *a4 = -1;
  }
  return a2 != 0;
}
