int *__fastcall sub_14157E7B0(int *a1, _QWORD *a2, __int64 *a3)
{
  __int64 v5; // r14
  int v6; // eax
  __int64 v7; // rdx
  unsigned __int64 v8; // rcx
  __int64 v9; // r15
  __int64 v10; // rax
  _QWORD *v11; // rsi
  __int64 v12; // rcx
  __int64 v13; // rdx
  __int64 v14; // rdi
  __int64 v15; // rbx
  __int64 v16; // rdx
  _QWORD *v17; // r13
  __int64 v18; // rbx
  unsigned __int64 v19; // rcx
  __int64 v20; // rdi
  __int64 v21; // rdi
  __int64 v22; // r14
  __int64 v23; // rdi
  __int64 v24; // rdi
  __int64 v25; // rdi
  __int64 v26; // rbx
  __int64 v27; // rdi
  __int64 v28; // rcx
  unsigned __int64 v29; // rsi
  unsigned __int64 v30; // rax
  unsigned __int64 v31; // r12
  unsigned __int64 v32; // rcx
  __int64 v33; // r8
  __int64 v34; // r15
  bool v35; // al
  unsigned __int64 v36; // rbx
  __int64 v37; // rsi
  __int64 v38; // rsi
  char v39; // si
  char v40; // r15
  unsigned __int64 v41; // rcx
  __int64 v42; // rdi
  __int64 v43; // rdi
  __int64 *v44; // rbx
  __int64 v45; // rdi
  unsigned __int64 v46; // rax
  __int64 v47; // rcx
  __int64 v48; // rdx
  unsigned __int64 v49; // r15
  unsigned __int64 v50; // rdx
  __int64 v51; // rax
  __int64 v52; // r8
  __int64 v53; // r15
  unsigned __int64 v54; // rax
  __int64 v55; // rdx
  __int64 v56; // rcx
  __int64 v57; // rax
  __int64 v58; // r9
  __int64 v59; // rdx
  __int64 v60; // rbx
  __int64 v61; // rsi
  __int64 v62; // rcx
  __int64 v63; // rcx
  __int64 v64; // rax
  __int64 v65; // rcx
  __int64 v66; // rbx
  __int64 v67; // rsi
  __int64 v68; // rdx
  __int64 v69; // rdx
  __int64 v70; // rcx
  __int64 v71; // rdx
  __int64 v72; // rbx
  __int64 v73; // rsi
  __int64 v74; // rdx
  __int64 *v75; // rsi
  __int64 v76; // rsi
  unsigned __int64 v77; // rcx
  __int64 v78; // rbx
  __int64 v79; // rbx
  bool v80; // al
  unsigned __int64 v82; // [rsp+28h] [rbp-58h]
  __int64 v83; // [rsp+30h] [rbp-50h]
  __int64 v84; // [rsp+30h] [rbp-50h]
  __int64 v85; // [rsp+38h] [rbp-48h]
  unsigned __int64 v86; // [rsp+38h] [rbp-48h]
  int *v87; // [rsp+40h] [rbp-40h]
  __int64 v88; // [rsp+48h] [rbp-38h] BYREF
  __int16 v89; // [rsp+50h] [rbp-30h] BYREF
  __int64 v90; // [rsp+58h] [rbp-28h]
  __int64 v91; // [rsp+60h] [rbp-20h]
  unsigned __int64 v92; // [rsp+68h] [rbp-18h]
  unsigned int v93; // [rsp+74h] [rbp-Ch] BYREF
  _QWORD *v94; // [rsp+78h] [rbp-8h]
  __int64 *v95; // [rsp+80h] [rbp+0h]
  unsigned int v96; // [rsp+8Ch] [rbp+Ch] BYREF
  __int64 v97; // [rsp+90h] [rbp+10h]

  v97 = -2;
  v96 = 0;
  v94 = a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v96, 4);
  v5 = v96;
  v6 = 1;
  if ( qword_141AA7808 <= (unsigned __int64)v96 )
    goto LABEL_125;
  v7 = *a3;
  v8 = 0xCCCCCCCCCCCCCCCDuLL * ((a3[2] - *a3) >> 3);
  v87 = a1;
  v95 = a3;
  if ( v8 < v96 )
  {
    v83 = v7;
    v85 = a3[1];
    v9 = sub_1407E4490(qword_141ABD470, 40LL * v96);
    v10 = *a3;
    v11 = (_QWORD *)a3[1];
    if ( (_QWORD *)*a3 != v11 )
    {
      v12 = 0;
      do
      {
        *(_WORD *)(v9 + v12 + 8) = *(_WORD *)(v10 + v12 + 8);
        *(_QWORD *)(v9 + v12) = *(_QWORD *)(v10 + v12);
        v13 = *(_QWORD *)(v10 + v12 + 32);
        *(_QWORD *)(v10 + v12 + 32) = 0;
        v14 = *(_QWORD *)(v10 + v12 + 16);
        v15 = *(_QWORD *)(v10 + v12 + 24);
        *(_QWORD *)(v10 + v12 + 24) = 0;
        *(_QWORD *)(v10 + v12 + 16) = 0;
        *(_QWORD *)(v9 + v12 + 16) = v14;
        *(_QWORD *)(v9 + v12 + 24) = v15;
        *(_QWORD *)(v9 + v12 + 32) = v13;
        v16 = v10 + v12 + 40;
        v12 += 40;
      }
      while ( (_QWORD *)v16 != v11 );
      v11 = (_QWORD *)*a3;
    }
    if ( v11 != nullptr )
    {
      v17 = (_QWORD *)a3[1];
      if ( v11 == v17 )
      {
        a3 = v95;
      }
      else
      {
        do
        {
          v18 = v11[2];
          if ( v18 != 0 )
          {
            v19 = v11[4] - v18;
            if ( v19 == -1 )
              v19 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v20 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19)
              && (v21 = *(_QWORD *)(v20 + 8 * v19)) != 0 )
            {
              MEMORY[0x1419475D8](v21 + 32, v18 - *(unsigned int *)(v21 + 120));
              if ( (*(_BYTE *)(v21 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v21 + 64)) == 0)
                && *(_BYTE *)(v21 + 97) != 0 )
              {
                sub_1412D33C0(v21);
              }
            }
            else
            {
              MEMORY[0x141948990](v18 - *(unsigned int *)(qword_141ABD470 + 48));
            }
            v11[4] = 0;
            v11[3] = 0;
            v11[2] = 0;
            a1 = v87;
          }
          v11 += 5;
        }
        while ( v11 != v17 );
        a3 = v95;
        v11 = (_QWORD *)*v95;
      }
      sub_1407E4890(qword_141ABD470, v11, a3[2] - (_QWORD)v11);
    }
    *a3 = v9;
    a3[1] = v9 + v85 - v83;
    a3[2] = v9 + 40 * v5;
    LODWORD(v5) = v96;
  }
  if ( (_DWORD)v5 == 0 )
  {
LABEL_124:
    v6 = *(_DWORD *)(*v94 + 16LL);
LABEL_125:
    *a1 = v6;
    return a1;
  }
  v22 = 0;
  while ( 1 )
  {
    v88 = 0;
    v89 = 0;
    v92 = 0;
    v91 = 0;
    v90 = 0;
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
          a1 = v87;
        }
      }
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    v92 = 0;
    v91 = 0;
    v90 = 0;
    v23 = *v94;
    (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*v94 + 40LL))(*v94, &v88, 4);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      goto LABEL_56;
    v24 = *v94;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v94 + 40LL))(*v94, (char *)&v88 + 4, 4);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      goto LABEL_56;
    v25 = *v94;
    (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*v94 + 40LL))(*v94, &v89, 2);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      goto LABEL_56;
    if ( v90 != v91 )
      v91 = v90;
    v93 = 0;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*v94 + 40LL))(*v94, &v93, 4);
    v26 = v93;
    if ( qword_141AA7808 <= (unsigned __int64)v93 )
      goto LABEL_56;
    v27 = v90;
    v28 = v91;
    v29 = (v91 - v90) >> 1;
    if ( v29 <= v93 )
    {
      if ( v29 < v93 )
      {
        v30 = (__int64)(v92 - v90) >> 1;
        if ( v30 >= v93 )
        {
          v36 = v93 - v29;
          v37 = v91 + 2 * v36;
          sub_141758A10(v91, 0, 2 * v36);
          v91 = v37;
          v27 = v90;
          v28 = v37;
        }
        else
        {
          v31 = v30 + (v30 >> 1);
          if ( v31 <= v93 )
            v31 = v93;
          v27 = sub_1407E4490(qword_141ABD470, 2 * v31);
          sub_141758A10(v27 + 2 * v29, 0, 2 * (v26 - v29));
          sub_141758A00(v27, v90, v91 - v90);
          if ( v90 != 0 )
          {
            v32 = v92 - v90;
            if ( v92 - v90 == -1 )
              v32 = *(unsigned int *)(v90 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v33 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v33) >> 3 > v32)
              && (v34 = *(_QWORD *)(v33 + 8 * v32)) != 0 )
            {
              MEMORY[0x1419475D8](v34 + 32, v90 - *(unsigned int *)(v34 + 120));
              v35 = *(_BYTE *)(v34 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v34 + 64)) != 0;
              if ( !v35 && *(_BYTE *)(v34 + 97) != 0 )
                sub_1412D33C0(v34);
            }
            else
            {
              MEMORY[0x141948990](v90 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          v90 = v27;
          v28 = v27 + 2 * v26;
          v91 = v28;
          v92 = v27 + 2 * v31;
          a1 = v87;
        }
      }
    }
    else
    {
      v28 = v90 + 2LL * v93;
      v91 = v28;
    }
    if ( (v28 - v27) >> 1 < (unsigned __int64)v93
      || (v38 = *v94,
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v94 + 40LL))(*v94, v27, 2LL * v93),
          *(_DWORD *)(v38 + 16) != 0) )
    {
LABEL_56:
      *a1 = 1;
      v39 = 0;
LABEL_57:
      v40 = 0;
      goto LABEL_58;
    }
    if ( *(_DWORD *)(*v94 + 16LL) == 0 )
    {
      v44 = v95;
      v45 = v95[1];
      if ( v45 != v95[2] )
      {
        *(_WORD *)(v45 + 8) = v89;
        *(_QWORD *)v45 = v88;
        v46 = v92;
        v92 = 0;
        v47 = v90;
        v48 = v91;
        v91 = 0;
        v90 = 0;
        *(_QWORD *)(v45 + 16) = v47;
        *(_QWORD *)(v45 + 24) = v48;
        *(_QWORD *)(v45 + 32) = v46;
        v44[1] += 40;
LABEL_116:
        v39 = 1;
        goto LABEL_57;
      }
      v49 = (v45 - *v95) / 40;
      v50 = v49 + (v49 >> 1);
      v82 = v49 + 1;
      if ( v50 <= v49 + 1 )
        v50 = v49 + 1;
      if ( v49 > 0x666666666666666LL - (v49 >> 1) )
        v50 = 0x666666666666666LL;
      v86 = v50;
      v51 = sub_1407E4490(qword_141ABD470, 40 * v50);
      v52 = 5 * v49;
      v53 = v51;
      *(_QWORD *)(v51 + 8 * v52) = v88;
      *(_WORD *)(v51 + 8 * v52 + 8) = v89;
      v54 = v92;
      v92 = 0;
      v55 = v90;
      v56 = v91;
      v91 = 0;
      v90 = 0;
      *(_QWORD *)(v53 + 8 * v52 + 16) = v55;
      *(_QWORD *)(v53 + 8 * v52 + 24) = v56;
      *(_QWORD *)(v53 + 8 * v52 + 32) = v54;
      v57 = *v44;
      v58 = v44[1];
      if ( v58 == v45 )
      {
        if ( v57 == v45 )
        {
LABEL_95:
          v75 = v95;
          if ( v45 != 0 )
          {
            v84 = v95[1];
            if ( v45 == v84 )
            {
              v75 = v95;
            }
            else
            {
              do
              {
                v76 = *(_QWORD *)(v45 + 16);
                if ( v76 != 0 )
                {
                  v77 = *(_QWORD *)(v45 + 32) - v76;
                  if ( v77 == -1 )
                    v77 = *(unsigned int *)(v76 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v78 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v78) >> 3 > v77)
                    && (v79 = *(_QWORD *)(v78 + 8 * v77)) != 0 )
                  {
                    MEMORY[0x1419475D8](v79 + 32, v76 - *(unsigned int *)(v79 + 120));
                    v80 = *(_BYTE *)(v79 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v79 + 64)) != 0;
                    if ( !v80 && *(_BYTE *)(v79 + 97) != 0 )
                      sub_1412D33C0(v79);
                  }
                  else
                  {
                    MEMORY[0x141948990](v76 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                  *(_QWORD *)(v45 + 32) = 0;
                  *(_QWORD *)(v45 + 24) = 0;
                  *(_QWORD *)(v45 + 16) = 0;
                }
                v45 += 40;
              }
              while ( v45 != v84 );
              v75 = v95;
              v45 = *v95;
            }
            sub_1407E4890(qword_141ABD470, v45, v75[2] - v45);
            a1 = v87;
          }
          *v75 = v53;
          v75[1] = v53 + 40 * v82;
          v75[2] = v53 + 40 * v86;
          goto LABEL_116;
        }
        v70 = 0;
        do
        {
          *(_WORD *)(v53 + v70 + 8) = *(_WORD *)(v57 + v70 + 8);
          *(_QWORD *)(v53 + v70) = *(_QWORD *)(v57 + v70);
          v71 = *(_QWORD *)(v57 + v70 + 32);
          *(_QWORD *)(v57 + v70 + 32) = 0;
          v72 = *(_QWORD *)(v57 + v70 + 16);
          v73 = *(_QWORD *)(v57 + v70 + 24);
          *(_QWORD *)(v57 + v70 + 24) = 0;
          *(_QWORD *)(v57 + v70 + 16) = 0;
          *(_QWORD *)(v53 + v70 + 16) = v72;
          *(_QWORD *)(v53 + v70 + 24) = v73;
          *(_QWORD *)(v53 + v70 + 32) = v71;
          v74 = v57 + v70 + 40;
          v70 += 40;
        }
        while ( v74 != v45 );
      }
      else
      {
        if ( v57 != v45 )
        {
          v59 = 0;
          do
          {
            *(_WORD *)(v53 + v59 + 8) = *(_WORD *)(v57 + v59 + 8);
            *(_QWORD *)(v53 + v59) = *(_QWORD *)(v57 + v59);
            v60 = *(_QWORD *)(v57 + v59 + 32);
            *(_QWORD *)(v57 + v59 + 32) = 0;
            v61 = *(_QWORD *)(v57 + v59 + 16);
            v62 = *(_QWORD *)(v57 + v59 + 24);
            *(_QWORD *)(v57 + v59 + 24) = 0;
            *(_QWORD *)(v57 + v59 + 16) = 0;
            *(_QWORD *)(v53 + v59 + 16) = v61;
            *(_QWORD *)(v53 + v59 + 24) = v62;
            *(_QWORD *)(v53 + v59 + 32) = v60;
            v63 = v57 + v59 + 40;
            v59 += 40;
          }
          while ( v63 != v45 );
          v58 = v95[1];
        }
        if ( v58 != v45 )
        {
          v64 = v53 + 8 * v52 + 72;
          v65 = 0;
          do
          {
            *(_WORD *)(v64 + v65 - 24) = *(_WORD *)(v45 + v65 + 8);
            *(_QWORD *)(v64 + v65 - 32) = *(_QWORD *)(v45 + v65);
            v66 = *(_QWORD *)(v45 + v65 + 32);
            *(_QWORD *)(v45 + v65 + 32) = 0;
            v67 = *(_QWORD *)(v45 + v65 + 16);
            v68 = *(_QWORD *)(v45 + v65 + 24);
            *(_QWORD *)(v45 + v65 + 24) = 0;
            *(_QWORD *)(v45 + v65 + 16) = 0;
            *(_QWORD *)(v64 + v65 - 16) = v67;
            *(_QWORD *)(v64 + v65 - 8) = v68;
            *(_QWORD *)(v64 + v65) = v66;
            v69 = v45 + v65 + 40;
            v65 += 40;
          }
          while ( v69 != v58 );
        }
      }
      v45 = *v95;
      goto LABEL_95;
    }
    v40 = 1;
    v39 = 0;
LABEL_58:
    if ( v90 == 0 )
      goto LABEL_69;
    v41 = v92 - v90;
    if ( v92 - v90 == -1 )
    {
      v41 = *(unsigned int *)(v90 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_68;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_68;
    }
    v42 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v42) >> 3 <= v41 || (v43 = *(_QWORD *)(v42 + 8 * v41)) == 0 )
    {
LABEL_68:
      MEMORY[0x141948990](v90 - *(unsigned int *)(qword_141ABD470 + 48));
      goto LABEL_69;
    }
    MEMORY[0x1419475D8](v43 + 32, v90 - *(unsigned int *)(v43 + 120));
    if ( (*(_BYTE *)(v43 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v43 + 64)) == 0)
      && *(_BYTE *)(v43 + 97) != 0 )
    {
      sub_1412D33C0(v43);
    }
LABEL_69:
    if ( v39 == 0 )
      break;
    if ( ++v22 >= (unsigned __int64)v96 )
      goto LABEL_124;
  }
  if ( v40 != 0 )
    goto LABEL_124;
  return a1;
}
