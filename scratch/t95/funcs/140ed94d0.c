char __fastcall sub_140ED94D0(__int64 a1, __int64 a2, int a3, __int64 a4)
{
  unsigned int v5; // esi
  void *v8; // rcx
  __int64 v9; // rdi
  unsigned __int64 v10; // rdx
  unsigned __int64 v11; // r13
  unsigned __int64 v12; // r15
  unsigned __int64 v13; // r9
  unsigned __int64 v14; // r12
  signed __int64 v15; // r8
  __int64 v16; // rsi
  __int64 v17; // r14
  __int64 v18; // r11
  __int64 v19; // rbx
  __int64 v20; // rax
  unsigned __int64 v21; // rsi
  __int64 v22; // rbx
  __int64 v23; // r10
  __int64 v24; // r11
  unsigned __int64 v25; // rbx
  __int64 v26; // rsi
  __int64 v27; // r14
  __int64 v28; // r14
  unsigned __int64 v29; // r11
  signed __int64 v30; // rsi
  __int64 v31; // r10
  signed __int64 v32; // rbx
  unsigned __int64 v33; // r8
  __int64 v34; // rcx
  unsigned __int64 v35; // r10
  __int64 v36; // r11
  unsigned __int64 v37; // r8
  unsigned __int64 v38; // rbx
  __int64 v39; // rcx
  __int64 v40; // rbx
  unsigned __int64 v41; // rcx
  __int64 v42; // rax
  __int64 i; // rsi
  __int64 v44; // r14
  __int64 v45; // r11
  __int64 v46; // r10
  __int64 v47; // rsi
  signed __int64 v48; // rdx
  signed __int64 v49; // rbx
  unsigned __int64 v50; // rsi
  __int64 v51; // rcx
  unsigned __int64 v52; // rcx
  __int64 v53; // rdx
  __int64 v54; // rsi
  _QWORD v56[2]; // [rsp+28h] [rbp-58h] BYREF
  int v57; // [rsp+38h] [rbp-48h] BYREF
  __int64 v58; // [rsp+40h] [rbp-40h] BYREF
  __int64 v59; // [rsp+50h] [rbp-30h]
  __int64 v60; // [rsp+58h] [rbp-28h] BYREF
  unsigned __int64 v61; // [rsp+60h] [rbp-20h]
  __int64 v62; // [rsp+68h] [rbp-18h]
  __int64 v63; // [rsp+70h] [rbp-10h]
  unsigned int v64; // [rsp+7Ch] [rbp-4h]
  __int64 v65; // [rsp+80h] [rbp+0h]

  v65 = -2;
  if ( a3 <= 0 )
    return 1;
  v5 = a3;
  v8 = (void *)qword_141ABD470;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    v8 = &unk_141B59A68;
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v60 = sub_1407E4490(v8, 2048);
  v61 = v60;
  v62 = v60 + 2048;
  sub_140ED9260(a1, a2, &v60);
  v9 = v60;
  v10 = v61;
  v11 = (__int64)(v61 - v60) >> 3;
  v12 = v5;
  if ( v11 <= v5 )
  {
    sub_140054D70(v60, v61, (__int64)(v61 - v60) >> 3, sub_140FCC240);
  }
  else
  {
    v13 = v60 + 8LL * v5;
    if ( v5 >= 2 )
    {
      v64 = v5;
      v59 = a4;
      v14 = (unsigned __int64)v5 >> 1;
      v63 = v5 - 1LL;
      v15 = (unsigned __int64)v63 >> 1;
      if ( (v5 & 1) != 0 )
      {
        do
        {
          v23 = v14--;
          v24 = *(_QWORD *)(v9 + 8 * v23 - 8);
          v22 = v14;
          if ( v15 >= v23 )
          {
            v25 = v14;
            do
            {
              if ( *(_WORD *)(*(_QWORD *)(v9 + 16 * v25 + 8) + 168LL) >= *(_WORD *)(*(_QWORD *)(v9 + 16 * v25 + 16)
                                                                                  + 168LL) )
                v26 = 2 * v25 + 2;
              else
                v26 = 2 * v25 + 1;
              *(_QWORD *)(v9 + 8 * v25) = *(_QWORD *)(v9 + 8 * v26);
              v25 = v26;
            }
            while ( v26 < v15 );
            if ( v26 >= v23 )
            {
              while ( 1 )
              {
                v22 = (v26 - 1) >> 1;
                v27 = *(_QWORD *)(v9 + 8 * v22);
                if ( *(_WORD *)(v24 + 168) >= *(_WORD *)(v27 + 168) )
                  break;
                *(_QWORD *)(v9 + 8 * v26) = v27;
                v26 = (v26 - 1) >> 1;
                if ( v22 < v23 )
                  goto LABEL_24;
              }
            }
            v22 = v26;
          }
LABEL_24:
          *(_QWORD *)(v9 + 8 * v22) = v24;
        }
        while ( v23 > 1 );
      }
      else
      {
        do
        {
          v17 = v14--;
          v18 = *(_QWORD *)(v9 + 8 * v17 - 8);
          v19 = v14;
          if ( v15 >= v17 )
          {
            v21 = v14;
            do
            {
              if ( *(_WORD *)(*(_QWORD *)(v9 + 16 * v21 + 8) + 168LL) >= *(_WORD *)(*(_QWORD *)(v9 + 16 * v21 + 16)
                                                                                  + 168LL) )
                v19 = 2 * v21 + 2;
              else
                v19 = 2 * v21 + 1;
              *(_QWORD *)(v9 + 8 * v21) = *(_QWORD *)(v9 + 8 * v19);
              v21 = v19;
            }
            while ( v19 < v15 );
          }
          if ( v19 == v15 )
          {
            *(_QWORD *)(v9 + 8 * v15) = *(_QWORD *)(v9 + 8 * v12 - 8);
            v19 = v63;
          }
          if ( v19 >= v17 )
          {
            while ( 1 )
            {
              v16 = (v19 - 1) >> 1;
              v20 = *(_QWORD *)(v9 + 8 * v16);
              if ( *(_WORD *)(v18 + 168) >= *(_WORD *)(v20 + 168) )
                break;
              *(_QWORD *)(v9 + 8 * v19) = v20;
              v19 = (v19 - 1) >> 1;
              if ( v16 < v17 )
                goto LABEL_10;
            }
          }
          v16 = v19;
LABEL_10:
          *(_QWORD *)(v9 + 8 * v16) = v18;
        }
        while ( v17 > 1 );
      }
      a4 = v59;
      if ( v13 >= v10 )
        goto LABEL_71;
      v28 = v63 >> 1;
      v5 = v64;
      if ( v64 >= 3 )
      {
        v29 = v9 + 8 * v12;
        do
        {
          v31 = *(_QWORD *)v29;
          if ( *(_WORD *)(*(_QWORD *)v9 + 168LL) < *(_WORD *)(*(_QWORD *)v29 + 168LL) )
          {
            *(_QWORD *)v29 = *(_QWORD *)v9;
            v32 = 0;
            do
            {
              if ( *(_WORD *)(*(_QWORD *)(v9 + 16 * v32 + 8) + 168LL) >= *(_WORD *)(*(_QWORD *)(v9 + 16 * v32 + 16)
                                                                                  + 168LL) )
                v30 = 2 * v32 + 2;
              else
                v30 = 2 * v32 + 1;
              *(_QWORD *)(v9 + 8 * v32) = *(_QWORD *)(v9 + 8 * v30);
              v32 = v30;
            }
            while ( v30 < v28 );
            if ( (v12 & 1) == 0 && v30 == v28 )
            {
              *(_QWORD *)(v9 + 8 * v28) = *(_QWORD *)(v9 + 8 * v12 - 8);
              v30 = v63;
            }
            if ( v30 <= 0 )
            {
LABEL_41:
              v30 = 0;
            }
            else
            {
              while ( 1 )
              {
                v33 = v30 - 1;
                v34 = *(_QWORD *)(v9 + 8 * ((unsigned __int64)(v30 - 1) >> 1));
                if ( *(_WORD *)(v31 + 168) >= *(_WORD *)(v34 + 168) )
                  break;
                *(_QWORD *)(v9 + 8 * v30) = v34;
                v30 = (unsigned __int64)(v30 - 1) >> 1;
                if ( v33 <= 1 )
                  goto LABEL_41;
              }
            }
            *(_QWORD *)(v9 + 8 * v30) = v31;
          }
          v29 += 8LL;
        }
        while ( v29 < v10 );
        goto LABEL_71;
      }
      if ( (v12 & 1) == 0 && (unsigned __int64)v63 <= 1 )
      {
        v35 = v9 + 8 * v12;
        do
        {
          v36 = *(_QWORD *)v35;
          if ( *(_WORD *)(*(_QWORD *)v9 + 168LL) < *(_WORD *)(*(_QWORD *)v35 + 168LL) )
          {
            *(_QWORD *)v35 = *(_QWORD *)v9;
            *(_QWORD *)(v9 + 8 * v28) = *(_QWORD *)(v9 + 8 * v12 - 8);
            v37 = v63;
            while ( 1 )
            {
              v38 = v37 - 1;
              v39 = *(_QWORD *)(v9 + 8 * ((v37 - 1) >> 1));
              if ( *(_WORD *)(v36 + 168) >= *(_WORD *)(v39 + 168) )
                break;
              *(_QWORD *)(v9 + 8 * v37) = v39;
              v37 = (v37 - 1) >> 1;
              if ( v38 < 2 )
              {
                v37 = 0;
                break;
              }
            }
            *(_QWORD *)(v9 + 8 * v37) = v36;
          }
          v35 += 8LL;
        }
        while ( v35 < v10 );
        goto LABEL_71;
      }
LABEL_67:
      v64 = v5;
      v40 = *(_QWORD *)v9;
      v41 = v9 + 8 * v12;
      do
      {
        v42 = *(_QWORD *)v41;
        if ( *(_WORD *)(v40 + 168) < *(_WORD *)(*(_QWORD *)v41 + 168LL) )
        {
          *(_QWORD *)v41 = v40;
          *(_QWORD *)v9 = v42;
          v40 = v42;
        }
        v41 += 8LL;
      }
      while ( v41 < v10 );
LABEL_71:
      if ( v64 >= 2 )
      {
        do
        {
          v44 = *(_QWORD *)(v13 - 8);
          *(_QWORD *)(v13 - 8) = *(_QWORD *)v9;
          v13 -= 8LL;
          v45 = v13 - v9;
          v46 = (__int64)(v13 - v9) >> 3;
          v47 = (v46 - 1) >> 1;
          if ( (__int64)(v13 - v9) < 17 )
          {
            v49 = 0;
          }
          else
          {
            v48 = 0;
            do
            {
              if ( *(_WORD *)(*(_QWORD *)(v9 + 16 * v48 + 8) + 168LL) >= *(_WORD *)(*(_QWORD *)(v9 + 16 * v48 + 16)
                                                                                  + 168LL) )
                v49 = 2 * v48 + 2;
              else
                v49 = 2 * v48 + 1;
              *(_QWORD *)(v9 + 8 * v48) = *(_QWORD *)(v9 + 8 * v49);
              v48 = v49;
            }
            while ( v49 < v47 );
          }
          if ( (v45 & 8) == 0 && v49 == v47 )
          {
            *(_QWORD *)(v9 + 8 * v47) = *(_QWORD *)(v9 + 8 * v46 - 8);
            v49 = v46 - 1;
          }
          if ( v49 > 0 )
          {
            while ( 1 )
            {
              v50 = v49 - 1;
              v51 = *(_QWORD *)(v9 + 8 * ((unsigned __int64)(v49 - 1) >> 1));
              if ( *(_WORD *)(v44 + 168) >= *(_WORD *)(v51 + 168) )
                break;
              *(_QWORD *)(v9 + 8 * v49) = v51;
              v49 = (unsigned __int64)(v49 - 1) >> 1;
              if ( v50 <= 1 )
              {
                v49 = 0;
                break;
              }
            }
          }
          *(_QWORD *)(v9 + 8 * v49) = v44;
        }
        while ( v45 > 8 );
      }
      goto LABEL_72;
    }
    if ( v13 < v61 )
      goto LABEL_67;
  }
LABEL_72:
  if ( v11 < v12 )
    v12 = v11;
  if ( v12 != 0 )
  {
    for ( i = 0; i != v12; ++i )
    {
      (*(void (__fastcall **)(_QWORD, int *))(**(_QWORD **)(v9 + 8 * i) + 144LL))(*(_QWORD *)(v9 + 8 * i), &v57);
      sub_140FEAD00(&v57, v56);
      sub_14083B5F0(a4, v56);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v56[0] + 16LL))(v56[0], v56);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v58 + 16LL))(v58, &v58);
    }
  }
  else if ( v9 == 0 )
  {
    return 1;
  }
  v52 = v62 - v9;
  if ( v62 - v9 == -1 )
  {
    v52 = *(unsigned int *)(v9 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
LABEL_103:
      MEMORY[0x141948990](v9 - *(unsigned int *)(qword_141ABD470 + 48));
      return 1;
    }
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    goto LABEL_103;
  }
  v53 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v53) >> 3 <= v52 )
    goto LABEL_103;
  v54 = *(_QWORD *)(v53 + 8 * v52);
  if ( v54 == 0 )
    goto LABEL_103;
  MEMORY[0x1419475D8](v54 + 32, v9 - *(unsigned int *)(v54 + 120));
  if ( (*(_BYTE *)(v54 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v54 + 64)) == 0)
    && *(_BYTE *)(v54 + 97) != 0 )
  {
    sub_1412D33C0(v54);
  }
  return 1;
}
