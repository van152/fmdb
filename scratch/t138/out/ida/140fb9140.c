char __fastcall sub_140FB9140(__int64 a1, int a2, __int64 a3)
{
  __int64 v3; // r12
  volatile signed __int32 *v4; // rdi
  unsigned __int16 *v5; // r13
  bool v6; // zf
  _DWORD *v7; // rsi
  _QWORD *v8; // rdi
  __int64 v9; // rdx
  __int64 v10; // rbx
  __int64 v11; // r8
  __int64 v12; // rdx
  volatile signed __int32 *v14; // rdi
  __int64 v15; // rax
  int v16; // r8d
  __int64 v17; // rax
  __int64 v18; // rax
  unsigned __int64 v19; // r14
  _QWORD *v20; // rax
  char v21; // si
  int v22; // eax
  volatile signed __int32 *v23; // rbx
  char v24; // si
  __int64 *v25; // rbx
  __int64 v26; // rcx
  __int64 v27; // rax
  __int64 v28; // rdx
  __int64 v29; // rdi
  __int64 v30; // rsi
  unsigned __int64 v31; // rsi
  __int64 v32; // rdi
  __int64 v33; // rax
  __int64 v34; // rcx
  __int64 v35; // rcx
  unsigned int v36; // ebx
  _DWORD *v37; // rax
  __int64 v38; // rcx
  __int64 v39; // rax
  __int64 v40; // rdx
  __int64 v41; // rdi
  __int64 v42; // rsi
  unsigned __int64 v43; // rsi
  __int64 v44; // rdi
  __int64 v45; // rax
  __int64 v46; // rcx
  __int64 v47; // rcx
  unsigned int v48; // ebx
  _DWORD *v49; // rax
  int v50; // ebx
  __int64 *v51; // rdi
  __int64 v52; // r15
  __int64 v53; // rax
  __int64 *v54; // r14
  __int64 v55; // r13
  unsigned __int64 v56; // rax
  unsigned __int64 v57; // r12
  unsigned __int64 v58; // rcx
  unsigned __int64 v59; // r12
  __int64 v60; // rsi
  __int64 *v61; // r15
  __int64 v62; // rax
  unsigned __int64 v63; // rcx
  __int64 v64; // r8
  __int64 v65; // r14
  volatile signed __int32 *v66; // rcx
  volatile signed __int32 *v67; // rcx
  __int64 v68; // [rsp+40h] [rbp-40h] BYREF
  __int64 v69; // [rsp+48h] [rbp-38h]
  int v70; // [rsp+50h] [rbp-30h]
  __int64 v71; // [rsp+58h] [rbp-28h]
  __int64 v72; // [rsp+60h] [rbp-20h]
  __int64 v73; // [rsp+68h] [rbp-18h]
  __int64 v74; // [rsp+70h] [rbp-10h]
  __int64 v75; // [rsp+78h] [rbp-8h]
  __int64 v76; // [rsp+80h] [rbp+0h]
  __int128 v77; // [rsp+88h] [rbp+8h]
  unsigned __int64 v78; // [rsp+98h] [rbp+18h]
  __int64 v79; // [rsp+A0h] [rbp+20h]
  unsigned __int16 *v80; // [rsp+A8h] [rbp+28h]
  __int64 v81; // [rsp+B0h] [rbp+30h]
  __int64 v82; // [rsp+B8h] [rbp+38h]
  __int64 *v83; // [rsp+C0h] [rbp+40h] BYREF
  volatile signed __int32 *v84; // [rsp+C8h] [rbp+48h] BYREF
  volatile signed __int32 *v85; // [rsp+D0h] [rbp+50h] BYREF
  unsigned __int64 v86; // [rsp+D8h] [rbp+58h]
  int v87; // [rsp+E4h] [rbp+64h] BYREF
  int v88; // [rsp+E8h] [rbp+68h] BYREF
  int v89; // [rsp+ECh] [rbp+6Ch]
  __int64 v90; // [rsp+F0h] [rbp+70h]

  v90 = -2;
  v3 = a1;
  sub_1407D0F70(
    a1: (unsigned int)&v68,
    a2: (unsigned int)&v85,
    a3: a2,
    a4: a1 + 72,
    a5: a3,
    a6: 1,
    a7: 0,
    0,
    0x80100004E554C4CLL);
  v4 = v85;
  if ( v85 == nullptr )
    return 1;
  v5 = (unsigned __int16 *)(v3 + 80);
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v85 + 40LL))(
    a1: v85,
    a2: v3 + 80,
    a3: 2);
  v6 = *((_DWORD *)v4 + 4) == 0;
  v88 = 0;
  if ( v6 )
  {
    v14 = v85;
    v15 = (*(__int64 (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v85 + 40LL))(
            a1: v85,
            a2: &v88,
            a3: 4);
    LOBYTE(v15) = *((_DWORD *)v14 + 4) == 0;
    v16 = v88;
    *(_DWORD *)(v3 + 84) = 0;
    v89 = v15;
    if ( v16 > 0 )
    {
      v68 = 0;
      sub_140FB9B50(a1: v3, a2: &v68, a3: (unsigned int)(v16 - 1));
      goto LABEL_18;
    }
    v7 = (_DWORD *)(v3 + 84);
  }
  else
  {
    v7 = (_DWORD *)(v3 + 84);
    *(_DWORD *)(v3 + 84) = 0;
    v89 = 0;
  }
  sub_140FB5480(a1: v3, a2: &v68, a3: *(_QWORD *)v3, a4: *(_QWORD *)(v3 + 8));
  if ( *(_QWORD *)(v3 + 56) != 0 )
  {
    *(_QWORD *)(v3 + 56) = 0;
    *(_QWORD *)(v3 + 48) = 0;
  }
  v8 = (_QWORD *)(v3 + 32);
  v9 = *(_QWORD *)(v3 + 32);
  if ( v9 != 0 )
  {
    v10 = *(_QWORD *)(v3 + 40);
    if ( v10 != 0 )
    {
      do
      {
        v12 = *(_QWORD *)(*v8 + 8 * v10-- - 8);
        if ( v12 != 0 )
          sub_1407E6420(a1: qword_141ABE200, a2: v12, a3: 16);
      }
      while ( v10 != 0 );
      v9 = *(_QWORD *)(v3 + 32);
      v11 = 8LL * *(_QWORD *)(v3 + 40);
    }
    else
    {
      v11 = 0;
    }
    sub_1407E6420(a1: qword_141ABE200, a2: v9, a3: v11);
  }
  *(_QWORD *)(v3 + 40) = 0;
  *v8 = 0;
  *v7 = 0;
LABEL_18:
  v17 = *(_QWORD *)(v3 + 64);
  if ( v17 != 0 )
    v18 = *(int *)(v17 + 24);
  else
    v18 = 0;
  v81 = v18;
  if ( v88 > 0 )
  {
    v82 = v3 + 24;
    v19 = 0;
    v79 = v3;
    v80 = (unsigned __int16 *)(v3 + 80);
    while ( 1 )
    {
      v20 = *(_QWORD **)(v3 + 64);
      v21 = 1;
      if ( v20 != nullptr )
      {
        if ( (__int64)v19 >= v81 || (v22 = *(_DWORD *)(*v20 + ((v19 >> 3) & 0x1FFFFFFC)), !_bittest(&v22, v19)) )
          v21 = 0;
      }
      v84 = v85;
      _InterlockedIncrement(v85 + 2);
      v23 = v84;
      (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: &v87,
        a3: 4);
      if ( *((_DWORD *)v23 + 4) == 0 )
        break;
LABEL_28:
      v24 = 0;
LABEL_94:
      v66 = v84;
      if ( v84 != nullptr && _InterlockedDecrement(v84 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v66)(a1: v66, a2: 1);
      if ( v24 == 0 )
      {
        v89 = 0;
        goto LABEL_105;
      }
      if ( (__int64)++v19 >= v88 )
        goto LABEL_105;
    }
    if ( v87 >= 0 )
    {
      v83 = nullptr;
      v86 = v19;
      if ( v21 != 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(a1: &unk_141B59A68);
            sub_141751048(a1: sub_1407E4B20);
            sub_141750EA0(a1: &dword_141B59AA8);
            v19 = v86;
          }
        }
        v25 = (__int64 *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
        if ( qword_141ABD470 == 0 )
        {
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
              v19 = v86;
            }
          }
          qword_141ABD470 = (__int64)&unk_141B59A68;
        }
        v25[2] = 0;
        v25[1] = 0;
        *v25 = 0;
        v83 = v25;
        sub_140FB9E00(a1: v3, a2: &v83, a3: v19);
        if ( v87 <= 0 )
          goto LABEL_93;
LABEL_63:
        v50 = 0;
        while ( 1 )
        {
          v69 = -1;
          v70 = 0;
          v68 = 0x1418822B8LL;
          v75 = -1;
          v74 = -1;
          v76 = 0x76C0001076C0001LL;
          LODWORD(v77) = 124518401;
          HIBYTE(v77) = 0;
          BYTE12(v77) = 0;
          v72 = 0;
          v71 = 0;
          *(_QWORD *)((char *)&v77 + 4) = 0x76C076CFFFFFFFFLL;
          *(_WORD *)((char *)&v77 + 13) = 0;
          v73 = 0;
          if ( (unsigned __int8)sub_14143A820(a1: &v68, a2: &v84, a3: *v5) == 0 )
            goto LABEL_28;
          v51 = v83;
          if ( v83 != nullptr )
            break;
LABEL_66:
          if ( ++v50 >= v87 )
            goto LABEL_93;
        }
        ++*(_DWORD *)(v3 + 84);
        if ( dword_141ABF448 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141ABF448);
          if ( dword_141ABF448 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141ABF3F8,
              a2: 1100122405,
              a3: 128,
              a4: 88,
              a5: 0,
              a6: 0,
              a7: 128,
              a8: 4096);
            sub_141751048(a1: sub_140E41970);
            sub_141750EA0(a1: &dword_141ABF448);
          }
        }
        v52 = sub_1407E58C0(a1: &unk_141ABF3F8, a2: 88);
        *(_QWORD *)v52 = 0x1418779A8LL;
        *(_QWORD *)(v52 + 8) = v69;
        *(_DWORD *)(v52 + 16) = v70;
        *(_QWORD *)v52 = 0x1418822B8LL;
        *(_OWORD *)(v52 + 72) = v77;
        *(_QWORD *)(v52 + 64) = v76;
        *(_QWORD *)(v52 + 56) = v75;
        *(_QWORD *)(v52 + 48) = v74;
        *(_QWORD *)(v52 + 40) = v73;
        v53 = v71;
        *(_QWORD *)(v52 + 32) = v72;
        *(_QWORD *)(v52 + 24) = v53;
        v54 = (__int64 *)v51[1];
        if ( v54 != (__int64 *)v51[2] )
        {
          *v54 = v52;
          v51[1] += 8;
LABEL_65:
          v19 = v86;
          goto LABEL_66;
        }
        v55 = (__int64)v54 - *v51;
        v56 = v55 >> 3;
        v57 = (unsigned __int64)(v55 >> 3) >> 1;
        v58 = 0x1FFFFFFFFFFFFFFFLL - v57;
        v59 = (v55 >> 3) + v57;
        v78 = (v55 >> 3) + 1;
        if ( v59 <= v78 )
          v59 = v56 + 1;
        if ( v56 > v58 )
          v59 = 0x1FFFFFFFFFFFFFFFLL;
        v60 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v59);
        *(_QWORD *)(v60 + v55) = v52;
        v61 = (__int64 *)v51[1];
        sub_141758A00(a1: v60, a2: *v51, a3: (char *)v54 - *v51);
        if ( v61 != v54 )
          sub_141758A00(a1: v60 + v55 + 8, a2: v54, a3: v51[1] - (_QWORD)v54);
        v62 = *v51;
        v5 = v80;
        if ( *v51 == 0 )
        {
LABEL_88:
          *v51 = v60;
          v51[1] = v60 + 8 * v78;
          v51[2] = v60 + 8 * v59;
          v3 = v79;
          goto LABEL_65;
        }
        v63 = v51[2] - v62;
        if ( v63 == -1 )
        {
          v63 = *(unsigned int *)(v62 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
LABEL_87:
            MEMORY[0x141948990](a1: v62 - *(unsigned int *)(qword_141ABD470 + 48));
            goto LABEL_88;
          }
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_87;
        }
        v64 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v64) >> 3 > v63 )
        {
          v65 = *(_QWORD *)(v64 + 8 * v63);
          if ( v65 != 0 )
          {
            MEMORY[0x1419475D8](a1: v65 + 32, a2: v62 - *(unsigned int *)(v65 + 120));
            if ( (*(_BYTE *)(v65 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v65 + 64)) == 0)
              && *(_BYTE *)(v65 + 97) != 0 )
            {
              sub_1412D33C0(a1: v65);
            }
            goto LABEL_88;
          }
        }
        goto LABEL_87;
      }
      v38 = *(_QWORD *)(v3 + 48);
      v39 = *(_QWORD *)(v3 + 56);
      if ( (((_BYTE)v39 + (_BYTE)v38) & 3) == 0 && *(_QWORD *)(v3 + 40) <= (unsigned __int64)(v39 + 4) >> 2 )
      {
        sub_140FBA260(a1: v82);
        v38 = *(_QWORD *)(v3 + 48);
        v39 = *(_QWORD *)(v3 + 56);
      }
      v40 = *(_QWORD *)(v3 + 32);
      v41 = *(_QWORD *)(v3 + 40);
      v42 = v38 & (4 * v41 - 1);
      *(_QWORD *)(v3 + 48) = v42;
      v43 = v39 + v42;
      v44 = (v43 >> 2) & (v41 + 0x3FFFFFFFFFFFFFFFLL);
      v45 = *(_QWORD *)(v40 + 8 * v44);
      if ( v45 != 0 )
      {
LABEL_62:
        *(_DWORD *)(v45 + 4 * (v43 & 3)) = v19;
        ++*(_QWORD *)(v3 + 56);
        if ( v87 > 0 )
          goto LABEL_63;
        goto LABEL_93;
      }
      if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
        && (v46 = *(_QWORD *)(qword_141ABE200 + 24), (unsigned __int64)(*(_QWORD *)(qword_141ABE200 + 32) - v46) >= 0x81)
        && (v47 = *(_QWORD *)(v46 + 128)) != 0 )
      {
        v48 = *(_DWORD *)(v47 + 88);
        v49 = (_DWORD *)sub_1407E58C0(a1: v47, a2: *(unsigned int *)(v47 + 80));
        if ( v48 == 0 )
          goto LABEL_61;
      }
      else
      {
        v48 = *(_DWORD *)(qword_141ABE200 + 48);
        v49 = (_DWORD *)sub_141601260(a1: v48 + 16, a2: 4096);
        if ( v48 == 0 )
        {
LABEL_61:
          *(_QWORD *)(*(_QWORD *)(v3 + 32) + 8 * v44) = v49;
          v45 = *(_QWORD *)(*(_QWORD *)(v3 + 32) + 8 * v44);
          goto LABEL_62;
        }
      }
      *v49 = 16;
      v49 = (_DWORD *)((char *)v49 + v48);
      goto LABEL_61;
    }
    v26 = *(_QWORD *)(v3 + 48);
    v27 = *(_QWORD *)(v3 + 56);
    if ( (((_BYTE)v27 + (_BYTE)v26) & 3) == 0 && *(_QWORD *)(v3 + 40) <= (unsigned __int64)(v27 + 4) >> 2 )
    {
      sub_140FBA260(a1: v82);
      v26 = *(_QWORD *)(v3 + 48);
      v27 = *(_QWORD *)(v3 + 56);
    }
    v28 = *(_QWORD *)(v3 + 32);
    v29 = *(_QWORD *)(v3 + 40);
    v30 = v26 & (4 * v29 - 1);
    *(_QWORD *)(v3 + 48) = v30;
    v31 = v27 + v30;
    v32 = (v31 >> 2) & (v29 + 0x3FFFFFFFFFFFFFFFLL);
    v33 = *(_QWORD *)(v28 + 8 * v32);
    if ( v33 != 0 )
    {
LABEL_58:
      *(_DWORD *)(v33 + 4 * (v31 & 3)) = v19;
      ++*(_QWORD *)(v3 + 56);
LABEL_93:
      v24 = 1;
      goto LABEL_94;
    }
    if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
      && (v34 = *(_QWORD *)(qword_141ABE200 + 24), (unsigned __int64)(*(_QWORD *)(qword_141ABE200 + 32) - v34) >= 0x81)
      && (v35 = *(_QWORD *)(v34 + 128)) != 0 )
    {
      v36 = *(_DWORD *)(v35 + 88);
      v37 = (_DWORD *)sub_1407E58C0(a1: v35, a2: *(unsigned int *)(v35 + 80));
      if ( v36 == 0 )
        goto LABEL_57;
    }
    else
    {
      v36 = *(_DWORD *)(qword_141ABE200 + 48);
      v37 = (_DWORD *)sub_141601260(a1: v36 + 16, a2: 4096);
      if ( v36 == 0 )
      {
LABEL_57:
        *(_QWORD *)(*(_QWORD *)(v3 + 32) + 8 * v32) = v37;
        v33 = *(_QWORD *)(*(_QWORD *)(v3 + 32) + 8 * v32);
        goto LABEL_58;
      }
    }
    *v37 = 16;
    v37 = (_DWORD *)((char *)v37 + v36);
    goto LABEL_57;
  }
LABEL_105:
  *(_WORD *)(v3 + 80) = *(_WORD *)(v3 + 82);
  v67 = v85;
  if ( v85 != nullptr && _InterlockedDecrement(v85 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v67)(a1: v67, a2: 1);
  return v89;
}
