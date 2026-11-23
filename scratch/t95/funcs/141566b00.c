__int64 __fastcall sub_141566B00(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  volatile signed __int32 **v8; // r12
  volatile signed __int32 *v10; // rsi
  volatile signed __int32 *v11; // rsi
  int v12; // edi
  bool v13; // zf
  __int64 v14; // rbx
  int v15; // edi
  __int64 v16; // r15
  __int64 v17; // rsi
  __int64 v18; // rdi
  __int64 v19; // rbp
  unsigned __int64 v20; // rcx
  __int64 v21; // r8
  __int64 v22; // r14
  bool v23; // al
  __int64 v24; // rbx
  __int64 v25; // r14
  __int64 v26; // rcx
  unsigned __int64 v27; // rsi
  __int64 v28; // rbx
  unsigned __int64 v29; // rax
  unsigned __int64 v30; // r15
  __int64 v31; // rsi
  unsigned __int64 v32; // rcx
  __int64 v33; // rbp
  __int64 v34; // rbp
  bool v35; // al
  unsigned __int64 v36; // rbp
  __int64 v37; // rdx
  __int64 v38; // rcx
  _BYTE *v39; // rdi
  unsigned __int64 v40; // rsi
  unsigned __int64 v41; // r14
  unsigned __int64 v42; // rbx
  __int64 v43; // r15
  _BYTE *v44; // r12
  __int64 v45; // rsi
  unsigned __int64 v46; // rcx
  __int64 v47; // rdi
  __int64 v48; // rdi
  bool v49; // al
  unsigned __int64 v50; // rbx
  __int64 v51; // rsi
  volatile signed __int32 *v52; // rsi
  __int64 v53; // r9
  __int64 v54; // rbx
  int v55; // esi
  __int64 v56; // r15
  __int64 v57; // rsi
  __int64 v58; // rdi
  __int64 v59; // rbp
  unsigned __int64 v60; // rcx
  __int64 v61; // r8
  __int64 v62; // r14
  bool v63; // al
  __int64 v64; // rdx
  volatile signed __int32 *v65; // rsi
  unsigned __int64 v66; // rbp
  _WORD *v67; // rsi
  __int64 v68; // rbx
  unsigned __int64 v69; // rax
  unsigned __int64 v70; // r15
  unsigned __int64 v71; // r14
  __int64 v72; // r12
  _WORD *v73; // rdi
  __int64 v74; // rdi
  unsigned __int64 v75; // rcx
  __int64 v76; // rbx
  __int64 v77; // rsi
  bool v78; // al
  unsigned int *v79; // rdi
  volatile signed __int32 *v81; // rsi
  __int64 v82; // r8
  __int16 v83; // [rsp+22h] [rbp-56h] BYREF
  unsigned int v84; // [rsp+24h] [rbp-54h] BYREF
  __int64 *v85; // [rsp+28h] [rbp-50h]
  volatile signed __int32 **v86; // [rsp+30h] [rbp-48h]

  v8 = a2;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_116;
  v11 = *v8;
  if ( *v8 != nullptr )
  {
    _InterlockedIncrement(v11 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 32, 8);
  }
  if ( *(_DWORD *)(a1 + 36) == 0 )
    *(_DWORD *)(a1 + 36) = *(_DWORD *)(a1 + 32);
  v12 = *((_DWORD *)v11 + 4);
  if ( _InterlockedDecrement(v11 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v11)(v11, 1);
  if ( v12 != 0 )
    goto LABEL_116;
  v13 = *(_QWORD *)(a1 + 72) == *(_QWORD *)(a1 + 64);
  v86 = v8;
  if ( !v13 )
  {
    v84 = 0;
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*v8 + 40LL))(*v8, &v84, 4);
    v14 = v84;
    v15 = 1;
    if ( qword_141AA7808 > (unsigned __int64)v84 )
    {
      v16 = *(_QWORD *)(a1 + 64);
      if ( *(_QWORD *)(a1 + 80) - v16 < (unsigned __int64)v84 )
      {
        v17 = *(_QWORD *)(a1 + 72);
        v18 = sub_1407E4490(qword_141ABD470, v84);
        sub_141758A00(v18, *(_QWORD *)(a1 + 64), *(_QWORD *)(a1 + 72) - *(_QWORD *)(a1 + 64));
        v19 = *(_QWORD *)(a1 + 64);
        if ( v19 != 0 )
        {
          v20 = *(_QWORD *)(a1 + 80) - v19;
          if ( v20 == -1 )
            v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v21 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v20)
            && (v22 = *(_QWORD *)(v21 + 8 * v20)) != 0 )
          {
            MEMORY[0x1419475D8](v22 + 32, v19 - *(unsigned int *)(v22 + 120));
            v23 = *(_BYTE *)(v22 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 64)) != 0;
            if ( !v23 && *(_BYTE *)(v22 + 97) != 0 )
              sub_1412D33C0(v22);
          }
          else
          {
            MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *(_QWORD *)(a1 + 64) = v18;
        *(_QWORD *)(a1 + 72) = v18 + v17 - v16;
        *(_QWORD *)(a1 + 80) = v14 + v18;
        LODWORD(v14) = v84;
      }
      if ( (_DWORD)v14 != 0 )
      {
        v36 = 0;
        do
        {
          LOBYTE(v83) = 0;
          (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*v8 + 40LL))(*v8, &v83, 1);
          if ( *((_DWORD *)*v8 + 4) != 0 )
            break;
          v39 = *(_BYTE **)(a1 + 72);
          if ( v39 == *(_BYTE **)(a1 + 80) )
          {
            v40 = (unsigned __int64)&v39[-*(_QWORD *)(a1 + 64)];
            if ( v40 == 0x7FFFFFFFFFFFFFFFLL )
              sub_1400526C0(v38, v37);
            v41 = v40 + 1;
            v42 = v40 + (v40 >> 1);
            if ( v42 <= v40 + 1 )
              v42 = v40 + 1;
            if ( v40 > ((v40 >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
              v42 = 0x7FFFFFFFFFFFFFFFLL;
            v43 = sub_1407E4490(qword_141ABD470, v42);
            *(_BYTE *)(v43 + v40) = v83;
            v44 = *(_BYTE **)(a1 + 72);
            sub_141758A00(v43, *(_QWORD *)(a1 + 64), &v39[-*(_QWORD *)(a1 + 64)]);
            if ( v44 != v39 )
              sub_141758A00(v43 + v40 + 1, v39, *(_QWORD *)(a1 + 72) - (_QWORD)v39);
            v45 = *(_QWORD *)(a1 + 64);
            v8 = v86;
            if ( v45 != 0 )
            {
              v46 = *(_QWORD *)(a1 + 80) - v45;
              if ( v46 == -1 )
                v46 = *(unsigned int *)(v45 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v47 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v47) >> 3 > v46)
                && (v48 = *(_QWORD *)(v47 + 8 * v46)) != 0 )
              {
                MEMORY[0x1419475D8](v48 + 32, v45 - *(unsigned int *)(v48 + 120));
                v49 = *(_BYTE *)(v48 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v48 + 64)) != 0;
                if ( !v49 && *(_BYTE *)(v48 + 97) != 0 )
                  sub_1412D33C0(v48);
              }
              else
              {
                MEMORY[0x141948990](v45 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *(_QWORD *)(a1 + 64) = v43;
            *(_QWORD *)(a1 + 72) = v43 + v41;
            *(_QWORD *)(a1 + 80) = v43 + v42;
          }
          else
          {
            *v39 = v83;
            ++*(_QWORD *)(a1 + 72);
          }
          ++v36;
        }
        while ( v36 < v84 );
      }
      v15 = *((_DWORD *)*v8 + 4);
    }
    goto LABEL_71;
  }
  v84 = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*v8 + 40LL))(*v8, &v84, 4);
  v24 = v84;
  v15 = 1;
  if ( qword_141AA7808 <= (unsigned __int64)v84 )
    goto LABEL_71;
  v25 = *(_QWORD *)(a1 + 64);
  v26 = *(_QWORD *)(a1 + 72);
  v27 = v26 - v25;
  if ( v26 - v25 <= (unsigned __int64)v84 )
  {
    if ( v27 >= v84 )
      goto LABEL_69;
    v29 = *(_QWORD *)(a1 + 80) - v25;
    if ( v29 >= v84 )
    {
      v50 = v84 - v27;
      v51 = v26 + v50;
      sub_141758A10(v26, 0, v50);
      *(_QWORD *)(a1 + 72) = v51;
      v25 = *(_QWORD *)(a1 + 64);
      v26 = v51;
      goto LABEL_69;
    }
    v30 = v29 + (v29 >> 1);
    if ( v30 <= v84 )
      v30 = v84;
    v25 = sub_1407E4490(qword_141ABD470, v30);
    sub_141758A10(v25 + v27, 0, v24 - v27);
    sub_141758A00(v25, *(_QWORD *)(a1 + 64), *(_QWORD *)(a1 + 72) - *(_QWORD *)(a1 + 64));
    v31 = *(_QWORD *)(a1 + 64);
    if ( v31 != 0 )
    {
      v32 = *(_QWORD *)(a1 + 80) - v31;
      if ( v32 == -1 )
        v32 = *(unsigned int *)(v31 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v33 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v33) >> 3 > v32)
        && (v34 = *(_QWORD *)(v33 + 8 * v32)) != 0 )
      {
        MEMORY[0x1419475D8](v34 + 32, v31 - *(unsigned int *)(v34 + 120));
        v35 = *(_BYTE *)(v34 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v34 + 64)) != 0;
        if ( !v35 && *(_BYTE *)(v34 + 97) != 0 )
          sub_1412D33C0(v34);
      }
      else
      {
        MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *(_QWORD *)(a1 + 64) = v25;
    v28 = v25 + v24;
    *(_QWORD *)(a1 + 72) = v28;
    *(_QWORD *)(a1 + 80) = v25 + v30;
  }
  else
  {
    v28 = v25 + v84;
    *(_QWORD *)(a1 + 72) = v28;
  }
  v26 = v28;
LABEL_69:
  if ( v26 - v25 >= (unsigned __int64)v84 )
  {
    v52 = *v8;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64))(*(_QWORD *)*v8 + 40LL))(*v8, v25);
    v15 = *((_DWORD *)v52 + 4);
  }
LABEL_71:
  if ( v15 != 0 )
    goto LABEL_116;
  v85 = (__int64 *)(a1 + 40);
  if ( *(_QWORD *)(a1 + 48) == *(_QWORD *)(a1 + 40) )
  {
    v84 = 0;
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*v8 + 40LL))(*v8, &v84, 4);
    v55 = 1;
    if ( qword_141AA7808 > (unsigned __int64)v84 )
    {
      sub_141568340(v85);
      v64 = *(_QWORD *)(a1 + 40);
      if ( (*(_QWORD *)(a1 + 48) - v64) >> 1 >= (unsigned __int64)v84 )
      {
        v65 = *v8;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*v8 + 40LL))(
          *v8,
          v64,
          2LL * v84);
        v55 = *((_DWORD *)v65 + 4);
      }
    }
  }
  else
  {
    v84 = 0;
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*v8 + 40LL))(*v8, &v84, 4);
    v54 = v84;
    v55 = 1;
    if ( qword_141AA7808 > (unsigned __int64)v84 )
    {
      v56 = *(_QWORD *)(a1 + 40);
      if ( (*(_QWORD *)(a1 + 56) - v56) >> 1 < (unsigned __int64)v84 )
      {
        v57 = *(_QWORD *)(a1 + 48);
        v58 = sub_1407E4490(qword_141ABD470, 2LL * v84);
        sub_141758A00(v58, *(_QWORD *)(a1 + 40), *(_QWORD *)(a1 + 48) - *(_QWORD *)(a1 + 40));
        v59 = *(_QWORD *)(a1 + 40);
        if ( v59 != 0 )
        {
          v60 = *(_QWORD *)(a1 + 56) - v59;
          if ( v60 == -1 )
            v60 = *(unsigned int *)(v59 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v61 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v61) >> 3 > v60)
            && (v62 = *(_QWORD *)(v61 + 8 * v60)) != 0 )
          {
            MEMORY[0x1419475D8](v62 + 32, v59 - *(unsigned int *)(v62 + 120));
            v63 = *(_BYTE *)(v62 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v62 + 64)) != 0;
            if ( !v63 && *(_BYTE *)(v62 + 97) != 0 )
              sub_1412D33C0(v62);
          }
          else
          {
            MEMORY[0x141948990](v59 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *(_QWORD *)(a1 + 40) = v58;
        *(_QWORD *)(a1 + 48) = v58 + v57 - v56;
        *(_QWORD *)(a1 + 56) = v58 + 2 * v54;
        LODWORD(v54) = v84;
      }
      if ( (_DWORD)v54 != 0 )
      {
        v66 = 0;
        do
        {
          v83 = 0;
          (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*v8 + 40LL))(*v8, &v83, 2);
          if ( *((_DWORD *)*v8 + 4) != 0 )
            break;
          v67 = *(_WORD **)(a1 + 48);
          if ( v67 == *(_WORD **)(a1 + 56) )
          {
            v68 = (__int64)v67 - *(_QWORD *)(a1 + 40);
            v69 = v68 >> 1;
            v70 = (v68 >> 1) + 1;
            v71 = (v68 >> 1) + ((unsigned __int64)(v68 >> 1) >> 1);
            if ( v71 <= v70 )
              v71 = v69 + 1;
            if ( v69 > (((unsigned __int64)(((__int64)v67 - *(_QWORD *)(a1 + 40)) >> 1) >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
              v71 = 0x7FFFFFFFFFFFFFFFLL;
            v72 = sub_1407E4490(qword_141ABD470, 2 * v71);
            *(_WORD *)(v72 + v68) = v83;
            v73 = *(_WORD **)(a1 + 48);
            sub_141758A00(v72, *(_QWORD *)(a1 + 40), (char *)v67 - *(_QWORD *)(a1 + 40));
            if ( v73 != v67 )
              sub_141758A00(v72 + v68 + 2, v67, *(_QWORD *)(a1 + 48) - (_QWORD)v67);
            v74 = *v85;
            if ( *v85 != 0 )
            {
              v75 = *(_QWORD *)(a1 + 56) - v74;
              if ( v75 == -1 )
                v75 = *(unsigned int *)(v74 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v76 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v76) >> 3 > v75)
                && (v77 = *(_QWORD *)(v76 + 8 * v75)) != 0 )
              {
                MEMORY[0x1419475D8](v77 + 32, v74 - *(unsigned int *)(v77 + 120));
                v78 = *(_BYTE *)(v77 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v77 + 64)) != 0;
                if ( !v78 && *(_BYTE *)(v77 + 97) != 0 )
                  sub_1412D33C0(v77);
              }
              else
              {
                MEMORY[0x141948990](v74 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *(_QWORD *)(a1 + 40) = v72;
            *(_QWORD *)(a1 + 48) = v72 + 2 * v70;
            *(_QWORD *)(a1 + 56) = v72 + 2 * v71;
            v8 = v86;
          }
          else
          {
            *v67 = v83;
            *(_QWORD *)(a1 + 48) += 2LL;
          }
          ++v66;
        }
        while ( v66 < v84 );
      }
      v55 = *((_DWORD *)*v8 + 4);
    }
  }
  if ( v55 != 0 )
  {
LABEL_116:
    LODWORD(v79) = 0;
    return (unsigned int)v79;
  }
  v81 = *v8;
  if ( *v8 != nullptr )
  {
    _InterlockedIncrement(v81 + 2);
    v79 = (unsigned int *)(a1 + 8);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v81 + 40LL))(v81, a1 + 8, 12);
  }
  else
  {
    v79 = (unsigned int *)(a1 + 8);
  }
  v82 = *v79;
  if ( (unsigned int)v82 >= 0x989681 )
  {
    v82 = a6;
    *v79 = a6;
  }
  if ( a8 != 0 )
  {
    LOBYTE(v53) = 1;
    (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, a1, v82, v53);
  }
  LOBYTE(v79) = 1;
  if ( v81 != nullptr && _InterlockedDecrement(v81 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v81)(v81, 1);
  return (unsigned int)v79;
}
