__int64 __fastcall sub_140E4FD70(__int64 a1, __int64 **a2, char a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 *v12; // rbp
  char *v13; // rsi
  char v15; // al
  unsigned int v16; // ecx
  int v17; // edx
  int v18; // edx
  __int64 *v19; // rsi
  __int64 v20; // rdx
  __int16 v21; // ax
  __int64 *v22; // rsi
  __int64 v23; // rax
  __int64 v24; // r8
  __int64 v25; // r8
  __int64 *v26; // rsi
  __int64 v27; // r8
  __int64 *v28; // rsi
  __int64 v29; // r8
  __int64 *v30; // rsi
  __int64 *v31; // rsi
  __int64 *v32; // rsi
  __int64 *v33; // rsi
  __int64 *v34; // rsi
  __int64 *v35; // rsi
  __int64 *v36; // rsi
  __int64 *v37; // rsi
  __int64 *v38; // rsi
  __int64 *v39; // rsi
  __int64 *v40; // rsi
  __int64 *v41; // rsi
  __int64 *v42; // rsi

  v12 = *a2;
  v13 = (char *)(a1 + 101);
  (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 101, 1);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_2;
  v15 = *v13;
  v16 = *v13;
  if ( v16 <= 0x13 && (v17 = 589856, _bittest(&v17, v16)) )
  {
    *(_QWORD *)(a1 + 48) = -1;
  }
  else
  {
    v12 = *a2;
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
      v25 = 4;
    else
      v25 = 8;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 48, v25);
    if ( *((_DWORD *)v12 + 4) != 0 )
      goto LABEL_2;
    v15 = *v13;
    v16 = *v13;
    if ( v16 > 0x13 )
      goto LABEL_21;
  }
  v18 = 852336;
  if ( !_bittest(&v18, v16) )
  {
LABEL_21:
    v26 = *a2;
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
      v27 = 4;
    else
      v27 = 8;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 32, v27);
    if ( *((_DWORD *)v26 + 4) != 0 )
      goto LABEL_2;
    v28 = *a2;
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
      v29 = 4;
    else
      v29 = 8;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 40, v29);
    if ( *((_DWORD *)v28 + 4) != 0 )
      goto LABEL_2;
    if ( (unsigned __int8)sub_140FB2BA0(a2, a1 + 56) == 0 )
      goto LABEL_2;
    v30 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 72, 4);
    if ( *((_DWORD *)v30 + 4) != 0 )
      goto LABEL_2;
    v31 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 76, 4);
    if ( *((_DWORD *)v31 + 4) != 0 )
      goto LABEL_2;
    v32 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 80, 2);
    if ( *((_DWORD *)v32 + 4) != 0 )
      goto LABEL_2;
    v33 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 82, 2);
    if ( *((_DWORD *)v33 + 4) != 0 )
      goto LABEL_2;
    v34 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 84, 2);
    if ( *((_DWORD *)v34 + 4) != 0 )
      goto LABEL_2;
    v35 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 86, 2);
    if ( *((_DWORD *)v35 + 4) != 0 )
      goto LABEL_2;
    v36 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 88, 2);
    if ( *((_DWORD *)v36 + 4) != 0 )
      goto LABEL_2;
    v37 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 90, 2);
    if ( *((_DWORD *)v37 + 4) != 0 )
      goto LABEL_2;
    v38 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 94, 2);
    if ( *((_DWORD *)v38 + 4) != 0 )
      goto LABEL_2;
    v39 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 96, 2);
    if ( *((_DWORD *)v39 + 4) != 0 )
      goto LABEL_2;
    v40 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 98, 2);
    if ( *((_DWORD *)v40 + 4) != 0 )
      goto LABEL_2;
    v41 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 100, 1);
    if ( *((_DWORD *)v41 + 4) != 0 )
      goto LABEL_2;
    v42 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 102, 1);
    if ( *((_DWORD *)v42 + 4) != 0 )
      goto LABEL_2;
    v22 = *a2;
    v20 = a1 + 104;
    v23 = **a2;
    v24 = 1;
    goto LABEL_11;
  }
  *(_BYTE *)(a1 + 102) = 0;
  *(_QWORD *)(a1 + 56) = -1;
  *(_QWORD *)(a1 + 32) = -1;
  *(_QWORD *)(a1 + 40) = -1;
  *(_QWORD *)(a1 + 80) = 0;
  *(_DWORD *)(a1 + 88) = 0;
  *(_DWORD *)(a1 + 94) = 0;
  *(_DWORD *)(a1 + 97) = 0;
  if ( v15 == 4 )
  {
    v19 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 82, 2);
    if ( *((_DWORD *)v19 + 4) == 0 )
    {
      v20 = a1 + 90;
      v21 = *(_WORD *)(a1 + 82);
      *(_WORD *)(a1 + 84) = v21;
      *(_WORD *)(a1 + 80) = v21;
      v22 = *a2;
      v23 = **a2;
      v24 = 2;
LABEL_11:
      (*(void (__fastcall **)(__int64 *, __int64, __int64))(v23 + 40))(v22, v20, v24);
      if ( *((_DWORD *)v22 + 4) == 0 )
        goto LABEL_12;
    }
LABEL_2:
    LODWORD(v12) = 0;
    return (unsigned int)v12;
  }
LABEL_12:
  if ( a3 == 0 || (LODWORD(v12) = 0, (unsigned __int8)sub_141084540(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8) != 0) )
    LOBYTE(v12) = 1;
  return (unsigned int)v12;
}
