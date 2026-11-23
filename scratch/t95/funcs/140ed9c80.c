char __fastcall sub_140ED9C80(__int64 a1, __int64 a2, int a3, __int64 a4, char a5)
{
  __int64 v6; // r12
  void *v7; // rcx
  char *v8; // rdi
  __int64 *v9; // r13
  char v10; // bl
  char *v11; // r14
  __int64 v12; // r15
  _QWORD *v13; // rsi
  __int64 v14; // rax
  __int64 v15; // rbx
  __int64 v16; // rax
  __int64 *v17; // rcx
  __int64 v18; // rax
  __int64 v19; // rcx
  unsigned __int64 v20; // rcx
  _BYTE *v21; // rax
  __int64 v22; // rcx
  __int64 v23; // r14
  unsigned __int64 v24; // r12
  unsigned __int64 v25; // rcx
  unsigned __int64 v26; // r12
  __int64 v27; // rbx
  unsigned __int64 v28; // rcx
  __int64 v29; // r8
  __int64 v30; // r15
  unsigned __int64 v31; // r15
  unsigned __int64 v32; // r12
  char *v33; // r9
  __int64 v34; // r13
  char *v35; // r15
  unsigned __int64 v36; // r10
  signed __int64 v37; // rdx
  __int64 v38; // rbx
  __int64 v39; // r11
  __int64 v40; // r14
  __int64 v41; // rcx
  __int64 v42; // rax
  unsigned __int64 v43; // rsi
  __int64 v44; // rbx
  __int64 v45; // rax
  __int64 v46; // rbx
  __int64 v47; // r11
  __int64 v48; // r8
  __int64 v49; // rsi
  __int64 v50; // rcx
  __int64 v51; // rbx
  __int64 v52; // rcx
  __int64 v53; // rax
  __int64 v54; // rax
  __int64 v55; // r11
  char *v56; // r14
  signed __int64 v57; // rbx
  __int64 v58; // rdx
  __int64 v59; // r10
  __int64 v60; // rsi
  signed __int64 v61; // rdx
  __int64 v62; // rsi
  __int64 v63; // rcx
  unsigned __int64 v64; // rsi
  __int64 v65; // rcx
  char *v66; // r14
  __int64 v67; // rbx
  __int64 v68; // r10
  unsigned __int64 v69; // rbx
  unsigned __int64 v70; // rdx
  __int64 v71; // rcx
  __int64 v72; // rcx
  char *v73; // rax
  __int64 v74; // rdx
  unsigned __int64 v75; // rsi
  char *v76; // rax
  __int64 v77; // rdx
  __int64 v78; // rbx
  __int64 i; // rbx
  __int64 v80; // rax
  __int64 v81; // rcx
  __int64 v82; // r14
  __int64 v83; // r11
  __int64 v84; // r10
  __int64 v85; // rsi
  signed __int64 v86; // rdx
  __int64 v87; // rcx
  signed __int64 v88; // rbx
  __int64 v89; // rax
  unsigned __int64 v90; // rcx
  __int64 v91; // rax
  unsigned __int64 v92; // rbx
  __int64 v93; // rcx
  __int64 v94; // rsi
  _QWORD v96[2]; // [rsp+28h] [rbp-58h] BYREF
  int v97; // [rsp+38h] [rbp-48h] BYREF
  __int64 v98; // [rsp+40h] [rbp-40h] BYREF
  __int64 v99; // [rsp+50h] [rbp-30h]
  __int64 v100; // [rsp+58h] [rbp-28h]
  __int64 v101; // [rsp+60h] [rbp-20h]
  __int64 v102; // [rsp+68h] [rbp-18h]
  unsigned __int64 v103; // [rsp+70h] [rbp-10h]
  unsigned int v104; // [rsp+7Ch] [rbp-4h]
  __int64 v105; // [rsp+80h] [rbp+0h]

  v105 = -2;
  if ( a3 > 0 )
  {
    v6 = a2;
    v99 = a1;
    v7 = (void *)qword_141ABD470;
    v104 = a3;
    v100 = a2;
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
          v6 = v100;
        }
      }
      v7 = &unk_141B59A68;
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    v101 = a4;
    v8 = (char *)sub_1407E4490(v7, 0x2000);
    v103 = (unsigned __int64)(v8 + 0x2000);
    v9 = (__int64 *)qword_141B5FEA8;
    v102 = qword_141B5FEB0;
    if ( qword_141B5FEA8 != qword_141B5FEB0 )
    {
      v10 = a5;
      v11 = v8;
      while ( 1 )
      {
        v12 = *v9;
        if ( v6 != 0 )
        {
          v13 = (_QWORD *)(v12 + *(int *)(*(_QWORD *)(v12 + 8) + 4LL) + 8);
          v14 = (*(__int64 (__fastcall **)(_QWORD *))(*v13 + 560LL))(v13);
          if ( v14 == 0 )
            goto LABEL_7;
          v15 = v14;
          if ( (unsigned __int8)sub_140087030() == 0 || (v13[3] & 0x1000) == 0 || (v16 = *(_QWORD *)(v15 + 272)) == 0 )
            v16 = *(_QWORD *)(v15 + 264);
          if ( v16 != v6 )
          {
LABEL_7:
            v10 = a5;
            goto LABEL_8;
          }
          v17 = *(__int64 **)(*(int *)(*(_QWORD *)(v12 + 8) + 8LL) + v12 + 96);
          v10 = a5;
          if ( v17 != nullptr )
          {
            v18 = *v17;
            v19 = v17[1] - *v17;
            if ( v19 != 0 )
            {
              v20 = v19 >> 4;
              if ( v20 < 2 )
                v20 = 1;
              v21 = (_BYTE *)(v18 + 11);
              while ( *v21 != 10 )
              {
                v21 += 16;
                if ( --v20 == 0 )
                  goto LABEL_23;
              }
              goto LABEL_8;
            }
          }
        }
LABEL_23:
        if ( v99 != 0
          && *(_QWORD *)(*(_QWORD *)(*(int *)(*(_QWORD *)(v12 + 8) + 8LL) + v12 + 80) + 240LL) != v99
          && *(_DWORD *)(v99 + 12) != 7 )
        {
          goto LABEL_8;
        }
        if ( v10 != -1 )
        {
          v22 = v12 + *(int *)(*(_QWORD *)(v12 + 8) + 4LL) + 8;
          if ( (*(char (__fastcall **)(__int64, __int64))(*(_QWORD *)v22 + 408LL))(v22, 0x1418761ECLL) > v10 )
            goto LABEL_8;
        }
        if ( v11 == (char *)v103 )
        {
          v23 = v11 - v8;
          v24 = (unsigned __int64)(v23 >> 3) >> 1;
          v25 = 0x1FFFFFFFFFFFFFFFLL - v24;
          v26 = (v23 >> 3) + v24;
          v103 = (v23 >> 3) + 1;
          if ( v26 <= v103 )
            v26 = (v23 >> 3) + 1;
          if ( v23 >> 3 > v25 )
            v26 = 0x1FFFFFFFFFFFFFFFLL;
          v27 = sub_1407E4490(qword_141ABD470, 8 * v26);
          *(_QWORD *)(v27 + v23) = v12;
          sub_141758A00();
          if ( v8 != nullptr )
          {
            v28 = v23;
            if ( v23 == -1 )
            {
              v28 = *(unsigned int *)&v8[-*(unsigned int *)(qword_141ABD470 + 48)];
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_44;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_44;
            }
            v29 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28 && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
            {
              MEMORY[0x1419475D8](v30 + 32, &v8[-*(unsigned int *)(v30 + 120)]);
              if ( (*(_BYTE *)(v30 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) == 0)
                && *(_BYTE *)(v30 + 97) != 0 )
              {
                sub_1412D33C0(v30);
              }
            }
            else
            {
LABEL_44:
              MEMORY[0x141948990](&v8[-*(unsigned int *)(qword_141ABD470 + 48)]);
            }
          }
          v11 = (char *)(v27 + 8 * v103);
          v103 = v27 + 8 * v26;
          v8 = (char *)v27;
          v10 = a5;
          v6 = v100;
          goto LABEL_8;
        }
        *(_QWORD *)v11 = v12;
        v11 += 8;
LABEL_8:
        if ( ++v9 == (__int64 *)v102 )
          goto LABEL_49;
      }
    }
    v11 = v8;
LABEL_49:
    v31 = (v11 - v8) >> 3;
    v32 = v104;
    if ( v31 <= v104 )
    {
      sub_140054D70(v8, v11, (v11 - v8) >> 3, &sub_140E36320);
      v34 = v101;
    }
    else
    {
      v102 = (v11 - v8) >> 3;
      v33 = &v8[8 * v104];
      v34 = v101;
      v35 = v11;
      if ( v104 >= 2 )
      {
        v36 = (unsigned __int64)v104 >> 1;
        v37 = ((unsigned __int64)v104 - 1) >> 1;
        if ( (v104 & 1) != 0 )
        {
          do
          {
            v47 = v36--;
            v48 = *(_QWORD *)&v8[8 * v47 - 8];
            v46 = v36;
            if ( v37 >= v47 )
            {
              v49 = v36;
              do
              {
                v51 = v49;
                v52 = 2 * v49;
                v49 = 2 * v49 + 2;
                v53 = *(_QWORD *)&v8[8 * v52 + 8];
                v50 = *(_QWORD *)&v8[8 * v52 + 16];
                if ( v53 != 0 && v50 != 0 )
                {
                  if ( *(_WORD *)(v53 + 510) < *(_WORD *)(v50 + 510) )
                    v49 = 2 * v51 + 1;
                  v50 = *(_QWORD *)&v8[8 * v49];
                }
                *(_QWORD *)&v8[8 * v51] = v50;
              }
              while ( v49 < v37 );
              if ( v49 >= v47 )
              {
                while ( v48 != 0 )
                {
                  v46 = (v49 - 1) >> 1;
                  v54 = *(_QWORD *)&v8[8 * v46];
                  if ( v54 == 0 || *(_WORD *)(v48 + 510) >= *(_WORD *)(v54 + 510) )
                    break;
                  *(_QWORD *)&v8[8 * v49] = v54;
                  v49 = (v49 - 1) >> 1;
                  if ( v46 < v47 )
                    goto LABEL_72;
                }
              }
              v46 = v49;
            }
LABEL_72:
            *(_QWORD *)&v8[8 * v46] = v48;
          }
          while ( v47 > 1 );
        }
        else
        {
          do
          {
            v39 = v36--;
            v40 = *(_QWORD *)&v8[8 * v39 - 8];
            v41 = v36;
            if ( v37 >= v39 )
            {
              v43 = v36;
              do
              {
                v41 = 2 * v43 + 2;
                v45 = *(_QWORD *)&v8[16 * v43 + 8];
                v44 = *(_QWORD *)&v8[16 * v43 + 16];
                if ( v45 != 0 && v44 != 0 )
                {
                  if ( *(_WORD *)(v45 + 510) < *(_WORD *)(v44 + 510) )
                    v41 = 2 * v43 + 1;
                  v44 = *(_QWORD *)&v8[8 * v41];
                }
                *(_QWORD *)&v8[8 * v43] = v44;
                v43 = v41;
              }
              while ( v41 < v37 );
            }
            if ( v41 == v37 )
            {
              *(_QWORD *)&v8[8 * v37] = *(_QWORD *)&v8[8 * v32 - 8];
              v41 = v32 - 1;
            }
            if ( v41 >= v39 )
            {
              while ( v40 != 0 )
              {
                v38 = (v41 - 1) >> 1;
                v42 = *(_QWORD *)&v8[8 * v38];
                if ( v42 == 0 || *(_WORD *)(v40 + 510) >= *(_WORD *)(v42 + 510) )
                  break;
                *(_QWORD *)&v8[8 * v41] = v42;
                v41 = (v41 - 1) >> 1;
                if ( v38 < v39 )
                  goto LABEL_54;
              }
            }
            v38 = v41;
LABEL_54:
            *(_QWORD *)&v8[8 * v38] = v40;
            v11 = v35;
          }
          while ( v39 > 1 );
        }
      }
      if ( v33 < v11 )
      {
        v55 = (__int64)(v32 - 1) >> 1;
        if ( v104 < 3 )
        {
          if ( (v32 & 1) != 0 || v32 - 1 >= 2 )
          {
            v72 = *(_QWORD *)v8;
            v73 = &v8[8 * v32];
            do
            {
              if ( v72 != 0 )
              {
                v74 = *(_QWORD *)v73;
                v75 = (unsigned __int64)v35;
                if ( *(_QWORD *)v73 != 0 && *(_WORD *)(v72 + 510) < *(_WORD *)(v74 + 510) )
                {
                  *(_QWORD *)v73 = v72;
                  *(_QWORD *)v8 = v74;
                }
                else
                {
                  v74 = v72;
                }
              }
              else
              {
                v74 = 0;
                v75 = (unsigned __int64)v35;
              }
              v73 += 8;
              v72 = v74;
            }
            while ( (unsigned __int64)v73 < v75 );
          }
          else if ( v104 <= 1 )
          {
            v76 = &v8[8 * v32];
            do
            {
              v77 = *(_QWORD *)v8;
              if ( *(_QWORD *)v8 != 0 )
              {
                v78 = *(_QWORD *)v76;
                if ( *(_QWORD *)v76 != 0 && *(_WORD *)(v77 + 510) < *(_WORD *)(v78 + 510) )
                {
                  *(_QWORD *)v76 = v77;
                  *(_QWORD *)&v8[8 * v55] = *(_QWORD *)&v8[8 * v32 - 8];
                  *(_QWORD *)&v8[8 * v32 - 8] = v78;
                }
              }
              v76 += 8;
            }
            while ( v76 < v35 );
          }
          else
          {
            v66 = &v8[8 * v32];
            do
            {
              v67 = *(_QWORD *)v8;
              if ( *(_QWORD *)v8 != 0 )
              {
                v68 = *(_QWORD *)v66;
                if ( *(_QWORD *)v66 != 0 && *(_WORD *)(v67 + 510) < *(_WORD *)(v68 + 510) )
                {
                  *(_QWORD *)v66 = v67;
                  *(_QWORD *)&v8[8 * v55] = *(_QWORD *)&v8[8 * v32 - 8];
                  v69 = v32 - 1;
                  while ( 1 )
                  {
                    v70 = v69 - 1;
                    v71 = *(_QWORD *)&v8[8 * ((v69 - 1) >> 1)];
                    if ( v71 == 0 || *(_WORD *)(v68 + 510) >= *(_WORD *)(v71 + 510) )
                      break;
                    *(_QWORD *)&v8[8 * v69] = v71;
                    v69 = (v69 - 1) >> 1;
                    if ( v70 < 2 )
                    {
                      v69 = 0;
                      break;
                    }
                  }
                  *(_QWORD *)&v8[8 * v69] = v68;
                }
              }
              v66 += 8;
            }
            while ( v66 < v35 );
          }
        }
        else
        {
          v56 = &v8[8 * v32];
          do
          {
            v58 = *(_QWORD *)v8;
            if ( *(_QWORD *)v8 != 0 )
            {
              v59 = *(_QWORD *)v56;
              if ( *(_QWORD *)v56 != 0 && *(_WORD *)(v58 + 510) < *(_WORD *)(v59 + 510) )
              {
                *(_QWORD *)v56 = v58;
                v57 = 0;
                do
                {
                  v61 = v57;
                  v62 = 2 * v57;
                  v57 = 2 * v57 + 2;
                  v63 = *(_QWORD *)&v8[8 * v62 + 8];
                  v60 = *(_QWORD *)&v8[8 * v62 + 16];
                  if ( v63 != 0 && v60 != 0 )
                  {
                    if ( *(_WORD *)(v63 + 510) < *(_WORD *)(v60 + 510) )
                      v57 = 2 * v61 + 1;
                    v60 = *(_QWORD *)&v8[8 * v57];
                  }
                  *(_QWORD *)&v8[8 * v61] = v60;
                }
                while ( v57 < v55 );
                if ( (v32 & 1) == 0 && v57 == v55 )
                {
                  *(_QWORD *)&v8[8 * v55] = *(_QWORD *)&v8[8 * v32 - 8];
                  v57 = v32 - 1;
                }
                if ( v57 <= 0 )
                {
LABEL_91:
                  v57 = 0;
                }
                else
                {
                  while ( 1 )
                  {
                    v64 = v57 - 1;
                    v65 = *(_QWORD *)&v8[8 * ((unsigned __int64)(v57 - 1) >> 1)];
                    if ( v65 == 0 || *(_WORD *)(v59 + 510) >= *(_WORD *)(v65 + 510) )
                      break;
                    *(_QWORD *)&v8[8 * v57] = v65;
                    v57 = (unsigned __int64)(v57 - 1) >> 1;
                    if ( v64 <= 1 )
                      goto LABEL_91;
                  }
                }
                *(_QWORD *)&v8[8 * v57] = v59;
              }
            }
            v56 += 8;
          }
          while ( v56 < v35 );
        }
      }
      v31 = v102;
      if ( v104 >= 2 )
      {
        do
        {
          v82 = *((_QWORD *)v33 - 1);
          *((_QWORD *)v33 - 1) = *(_QWORD *)v8;
          v33 -= 8;
          v83 = v33 - v8;
          v84 = (v33 - v8) >> 3;
          v85 = (v84 - 1) >> 1;
          if ( v33 - v8 < 17 )
          {
            v88 = 0;
          }
          else
          {
            v86 = 0;
            do
            {
              v88 = 2 * v86 + 2;
              v89 = *(_QWORD *)&v8[16 * v86 + 8];
              v87 = *(_QWORD *)&v8[16 * v86 + 16];
              if ( v89 != 0 && v87 != 0 )
              {
                if ( *(_WORD *)(v89 + 510) < *(_WORD *)(v87 + 510) )
                  v88 = 2 * v86 + 1;
                v87 = *(_QWORD *)&v8[8 * v88];
              }
              *(_QWORD *)&v8[8 * v86] = v87;
              v86 = v88;
            }
            while ( v88 < v85 );
          }
          if ( (v83 & 8) == 0 && v88 == v85 )
          {
            *(_QWORD *)&v8[8 * v85] = *(_QWORD *)&v8[8 * v84 - 8];
            v88 = v84 - 1;
          }
          if ( v88 > 0 )
          {
            while ( v82 != 0 )
            {
              v90 = v88 - 1;
              v91 = *(_QWORD *)&v8[8 * ((unsigned __int64)(v88 - 1) >> 1)];
              if ( v91 == 0 || *(_WORD *)(v82 + 510) >= *(_WORD *)(v91 + 510) )
                break;
              *(_QWORD *)&v8[8 * v88] = v91;
              v88 = (unsigned __int64)(v88 - 1) >> 1;
              if ( v90 <= 1 )
              {
                v88 = 0;
                break;
              }
            }
          }
          *(_QWORD *)&v8[8 * v88] = v82;
        }
        while ( v83 > 8 );
      }
    }
    if ( v31 < v32 )
      v32 = v31;
    if ( v32 != 0 )
    {
      for ( i = 0; i != v32; ++i )
      {
        v80 = *(_QWORD *)&v8[8 * i];
        if ( v80 != 0 )
        {
          v81 = v80 + *(int *)(*(_QWORD *)(v80 + 8) + 4LL) + 8;
          (*(void (__fastcall **)(__int64, int *))(*(_QWORD *)v81 + 144LL))(v81, &v97);
          sub_140FEAD00(&v97, v96);
          sub_14083B5F0(v34, v96);
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v96[0] + 16LL))(v96[0], v96);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v98 + 16LL))(v98, &v98);
        }
      }
    }
    else if ( v8 == nullptr )
    {
      return 1;
    }
    v92 = v103 - (_QWORD)v8;
    if ( v103 - (_QWORD)v8 == -1 )
    {
      v92 = *(unsigned int *)&v8[-*(unsigned int *)(qword_141ABD470 + 48)];
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_177:
        MEMORY[0x141948990](&v8[-*(unsigned int *)(qword_141ABD470 + 48)]);
        return 1;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_177;
    }
    v93 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v93) >> 3 <= v92 )
      goto LABEL_177;
    v94 = *(_QWORD *)(v93 + 8 * v92);
    if ( v94 == 0 )
      goto LABEL_177;
    MEMORY[0x1419475D8](v94 + 32, &v8[-*(unsigned int *)(v94 + 120)]);
    if ( (*(_BYTE *)(v94 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v94 + 64)) == 0)
      && *(_BYTE *)(v94 + 97) != 0 )
    {
      sub_1412D33C0(v94);
    }
  }
  return 1;
}
