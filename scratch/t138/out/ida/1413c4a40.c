bool __fastcall sub_1413C4A40(_QWORD *a1, _QWORD *a2)
{
  _QWORD *v2; // r12
  __int64 v4; // rbx
  int v5; // edi
  __int64 v6; // r15
  __int64 v7; // rsi
  __int64 v8; // rdi
  __int64 v9; // rbp
  unsigned __int64 v10; // rcx
  __int64 v11; // r8
  __int64 v12; // r14
  bool v13; // al
  __int64 v14; // rbx
  __int64 v15; // r14
  __int64 v16; // rcx
  unsigned __int64 v17; // rsi
  __int64 v18; // rbx
  unsigned __int64 v19; // rax
  unsigned __int64 v20; // r15
  __int64 v21; // rsi
  unsigned __int64 v22; // rcx
  __int64 v23; // rbp
  __int64 v24; // rbp
  bool v25; // al
  __int64 v26; // r14
  _BYTE *v27; // rdi
  unsigned __int64 v28; // rsi
  _QWORD *v29; // r15
  unsigned __int64 v30; // rbx
  __int64 v31; // rbp
  _BYTE *v32; // r12
  __int64 v33; // rsi
  unsigned __int64 v34; // rcx
  __int64 v35; // rdi
  __int64 v36; // rdi
  unsigned __int64 v37; // rbx
  __int64 v38; // rsi
  __int64 v39; // rsi
  __int64 v40; // rsi
  __int64 v41; // rsi
  __int64 v43; // rsi
  char v44; // [rsp+27h] [rbp-51h] BYREF
  unsigned int v45; // [rsp+28h] [rbp-50h] BYREF
  unsigned int v46; // [rsp+2Ch] [rbp-4Ch] BYREF
  unsigned __int64 v47; // [rsp+30h] [rbp-48h]

  v2 = a2;
  if ( a1[3] == a1[2] )
  {
    v46 = 0;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v46, a3: 4);
    v14 = v46;
    v5 = 1;
    if ( qword_141AA7808 <= (unsigned __int64)v46 )
      goto LABEL_63;
    v15 = a1[2];
    v16 = a1[3];
    v17 = v16 - v15;
    if ( v16 - v15 <= (unsigned __int64)v46 )
    {
      if ( v17 >= v46 )
        goto LABEL_61;
      v19 = a1[4] - v15;
      if ( v19 >= v46 )
      {
        v37 = v46 - v17;
        v38 = v16 + v37;
        sub_141758A10(a1: v16, a2: 0, a3: v37);
        a1[3] = v38;
        v15 = a1[2];
        v16 = v38;
        goto LABEL_61;
      }
      v20 = v19 + (v19 >> 1);
      if ( v20 <= v46 )
        v20 = v46;
      v15 = sub_1407E4490(a1: qword_141ABD470, a2: v20);
      sub_141758A10(a1: v15 + v17, a2: 0, a3: v14 - v17);
      sub_141758A00(a1: v15, a2: a1[2], a3: a1[3] - a1[2]);
      v21 = a1[2];
      if ( v21 != 0 )
      {
        v22 = a1[4] - v21;
        if ( v22 == -1 )
          v22 = *(unsigned int *)(v21 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v23 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v23) >> 3 > v22)
          && (v24 = *(_QWORD *)(v23 + 8 * v22)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v24 + 32, a2: v21 - *(unsigned int *)(v24 + 120));
          v25 = *(_BYTE *)(v24 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 64)) != 0;
          if ( !v25 && *(_BYTE *)(v24 + 97) != 0 )
            sub_1412D33C0(a1: v24);
        }
        else
        {
          MEMORY[0x141948990](a1: v21 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      a1[2] = v15;
      v18 = v15 + v14;
      a1[3] = v18;
      a1[4] = v15 + v20;
    }
    else
    {
      v18 = v15 + v46;
      a1[3] = v18;
    }
    v16 = v18;
LABEL_61:
    if ( v16 - v15 >= (unsigned __int64)v46 )
    {
      v39 = *v2;
      (*(void (__fastcall **)(_QWORD, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: v15);
      v5 = *(_DWORD *)(v39 + 16);
    }
    goto LABEL_63;
  }
  v45 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v45, a3: 4);
  v4 = v45;
  v5 = 1;
  if ( qword_141AA7808 > (unsigned __int64)v45 )
  {
    v6 = a1[2];
    if ( a1[4] - v6 < (unsigned __int64)v45 )
    {
      v7 = a1[3];
      v8 = sub_1407E4490(a1: qword_141ABD470, a2: v45);
      sub_141758A00(a1: v8, a2: a1[2], a3: a1[3] - a1[2]);
      v9 = a1[2];
      if ( v9 != 0 )
      {
        v10 = a1[4] - v9;
        if ( v10 == -1 )
          v10 = *(unsigned int *)(v9 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v11 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v11) >> 3 > v10)
          && (v12 = *(_QWORD *)(v11 + 8 * v10)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v12 + 32, a2: v9 - *(unsigned int *)(v12 + 120));
          v13 = *(_BYTE *)(v12 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 + 64)) != 0;
          if ( !v13 && *(_BYTE *)(v12 + 97) != 0 )
            sub_1412D33C0(a1: v12);
        }
        else
        {
          MEMORY[0x141948990](a1: v9 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      a1[2] = v8;
      a1[3] = v8 + v7 - v6;
      a1[4] = v4 + v8;
      LODWORD(v4) = v45;
    }
    if ( (_DWORD)v4 != 0 )
    {
      v26 = 0;
      while ( 1 )
      {
        v44 = 0;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v44, a3: 1);
        if ( *(_DWORD *)(*v2 + 16LL) != 0 )
          goto LABEL_56;
        v27 = (_BYTE *)a1[3];
        if ( v27 == (_BYTE *)a1[4] )
          break;
        *v27 = v44;
        ++a1[3];
LABEL_32:
        if ( ++v26 >= (unsigned __int64)v45 )
          goto LABEL_56;
      }
      v28 = (unsigned __int64)&v27[-a1[2]];
      if ( v28 == 0x7FFFFFFFFFFFFFFFLL )
        sub_1400526C0();
      v29 = v2;
      v30 = v28 + (v28 >> 1);
      v47 = v28 + 1;
      if ( v30 <= v28 + 1 )
        v30 = v28 + 1;
      if ( v28 > ((v28 >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
        v30 = 0x7FFFFFFFFFFFFFFFLL;
      v31 = sub_1407E4490(a1: qword_141ABD470, a2: v30);
      *(_BYTE *)(v31 + v28) = v44;
      v32 = (_BYTE *)a1[3];
      sub_141758A00(a1: v31, a2: a1[2], a3: &v27[-a1[2]]);
      if ( v32 != v27 )
        sub_141758A00(a1: v31 + v28 + 1, a2: v27, a3: a1[3] - (_QWORD)v27);
      v33 = a1[2];
      v2 = v29;
      if ( v33 == 0 )
      {
LABEL_53:
        a1[2] = v31;
        a1[3] = v31 + v47;
        a1[4] = v31 + v30;
        goto LABEL_32;
      }
      v34 = a1[4] - v33;
      if ( v34 == -1 )
      {
        v34 = *(unsigned int *)(v33 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_52:
          MEMORY[0x141948990](a1: v33 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_53;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_52;
      }
      v35 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v35) >> 3 > v34 )
      {
        v36 = *(_QWORD *)(v35 + 8 * v34);
        if ( v36 != 0 )
        {
          MEMORY[0x1419475D8](a1: v36 + 32, a2: v33 - *(unsigned int *)(v36 + 120));
          if ( (*(_BYTE *)(v36 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v36 + 64)) == 0)
            && *(_BYTE *)(v36 + 97) != 0 )
          {
            sub_1412D33C0(a1: v36);
          }
          goto LABEL_53;
        }
      }
      goto LABEL_52;
    }
LABEL_56:
    v5 = *(_DWORD *)(*v2 + 16LL);
  }
LABEL_63:
  if ( v5 != 0 )
    return false;
  v40 = *v2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: a1 + 1, a3: 2);
  if ( *(_DWORD *)(v40 + 16) != 0 )
    return false;
  v41 = *v2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: (__int64)a1 + 10, a3: 1);
  if ( *(_DWORD *)(v41 + 16) != 0 )
    return false;
  v43 = *v2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: (__int64)a1 + 11, a3: 1);
  return *(_DWORD *)(v43 + 16) == 0;
}
