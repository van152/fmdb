bool __fastcall sub_143BCC880(__int64 a1, _WORD *a2, _WORD *a3)
{
  __int64 v6; // rsi
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rax
  __int64 v11; // rcx
  __int64 v12; // rax

  v6 = sub_140E0F130();
  if ( v6 != 0 )
  {
    v7 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
    v8 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v7 + 656LL))(v7);
    if ( v8 == 0 || *(_BYTE *)(v8 + 47) != 0 || *(_QWORD *)(v8 + 48) == 0 )
      goto LABEL_8;
    v9 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
    v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 656LL))(v9);
    v11 = 0;
    if ( *(_BYTE *)(v10 + 47) == 0 )
      v11 = *(_QWORD *)(v10 + 48);
    v12 = sub_1411E6040(v11, 0, 0);
    if ( v12 == 0 )
LABEL_8:
      v12 = sub_140F75250();
    (*(void (__fastcall **)(__int64, __int64, __int64, _WORD *, _WORD *, _BYTE, __int64))(*(_QWORD *)qword_141B5EC88
                                                                                        + 272LL))(
      qword_141B5EC88,
      v12,
      v6,
      a2,
      a3,
      0,
      a1);
  }
  else
  {
    *a2 = -1;
    *a3 = -1;
  }
  return v6 != 0;
}
