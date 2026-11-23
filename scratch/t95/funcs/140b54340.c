_QWORD *__fastcall sub_140B54340(
        __int64 a1,
        _QWORD *a2,
        __int16 *a3,
        char a4,
        __int64 a5,
        __int64 a6,
        unsigned __int8 a7,
        char a8,
        int a9,
        char a10,
        char a11,
        char a12,
        __int16 a13)
{
  __int64 v14; // r12
  __int64 v15; // rdi
  __int64 v16; // rsi
  _QWORD *v17; // r13
  unsigned int v18; // ebx
  unsigned int v19; // ecx
  unsigned int v20; // r15d
  __int16 v21; // dx
  unsigned __int16 v22; // r15
  __int16 v23; // cx
  unsigned int v24; // eax
  int v25; // ebx
  int v26; // ebx
  int v27; // ebx
  unsigned __int16 v28; // dx
  int v29; // eax
  unsigned __int16 v30; // bx
  int v31; // ecx
  int v32; // eax
  __int16 v33; // bx
  int v34; // eax
  _QWORD *v35; // rax
  __int64 v36; // r9
  _QWORD *v37; // r15
  __int64 v38; // rax
  unsigned __int64 v39; // r14
  __int64 v40; // r13
  __int64 v41; // rax
  _QWORD *v42; // rsi
  __int64 *v43; // r15
  __int64 v44; // rax
  __int64 v45; // rsi
  _QWORD *v46; // rdi
  _QWORD *v47; // rbx
  unsigned __int64 v48; // r12
  unsigned __int64 v49; // rdi
  unsigned __int64 v50; // rbx
  bool v51; // zf
  __int64 v52; // rcx
  __int64 v53; // rcx
  __int64 v54; // r13
  char *v55; // rax
  char *v56; // rbx
  __int64 *v57; // r13
  _QWORD *v58; // r14
  __int64 v59; // rbx
  char v60; // al
  __int16 i; // bx
  __int16 v62; // cx
  __int16 v63; // cx
  __int128 v64; // kr00_16
  __int64 v65; // r14
  unsigned __int16 v66; // ax
  unsigned __int16 v67; // cx
  __int16 v68; // dx
  __int64 v69; // r15
  _QWORD *v70; // rsi
  _QWORD *v71; // rbx
  _QWORD *result; // rax
  _QWORD *v73; // rbx
  __int64 v74; // rbx
  __int64 v75; // rdx
  unsigned __int64 v76; // rcx
  __int64 v77; // rbx
  __int64 v78; // rsi
  bool v79; // cl
  _QWORD *v80; // rsi
  _DWORD v81[302]; // [rsp+50h] [rbp-30h] BYREF
  unsigned __int64 v82; // [rsp+508h] [rbp+488h]
  unsigned __int64 v83; // [rsp+510h] [rbp+490h]
  __int64 v84; // [rsp+518h] [rbp+498h]
  __int128 v85; // [rsp+520h] [rbp+4A0h] BYREF
  __int64 v86; // [rsp+530h] [rbp+4B0h]
  __int128 v87; // [rsp+540h] [rbp+4C0h] BYREF
  __int64 v88; // [rsp+550h] [rbp+4D0h]
  _QWORD *v89; // [rsp+558h] [rbp+4D8h]
  __int64 v90; // [rsp+560h] [rbp+4E0h]
  __int64 v91; // [rsp+568h] [rbp+4E8h]
  unsigned int v92; // [rsp+574h] [rbp+4F4h]
  int v93; // [rsp+578h] [rbp+4F8h]
  int v94; // [rsp+57Ch] [rbp+4FCh]
  __int64 v95; // [rsp+580h] [rbp+500h]
  __int16 *v96; // [rsp+588h] [rbp+508h]
  unsigned int v97; // [rsp+594h] [rbp+514h]
  int v98; // [rsp+598h] [rbp+518h]
  int v99; // [rsp+59Ch] [rbp+51Ch]
  unsigned int v100; // [rsp+5A0h] [rbp+520h] BYREF
  _QWORD *v101; // [rsp+5A8h] [rbp+528h]
  int v102; // [rsp+5B0h] [rbp+530h]
  int v103; // [rsp+5B4h] [rbp+534h]
  _QWORD *v104; // [rsp+5B8h] [rbp+538h]
  __int64 v105; // [rsp+5C0h] [rbp+540h]

  v105 = -2;
  v96 = a3;
  v101 = a2;
  v84 = a1;
  v14 = a6;
  v15 = a5;
  if ( a5 != 0 )
    v16 = *(_QWORD *)(a5 + 176);
  else
    v16 = 0;
  v102 = sub_140B41F60((unsigned int)v81, a6, 0, v16, 0, 0, 0, 0, 0);
  if ( v102 == 0 )
  {
    result = v101;
    *v101 = 0;
    return result;
  }
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
        v14 = a6;
        v15 = a5;
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v85 = 0;
  v86 = 0;
  if ( v16 != 0 )
    sub_140988C10(v16, &v85, 0);
  v91 = v16;
  if ( dword_141ABEC98 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141ABEC98);
    if ( dword_141ABEC98 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141ABEC48, 1100123278, 128, 24, 0, 0, 128, 4096);
      sub_141751048(sub_1400D9390);
      sub_141750EA0(&dword_141ABEC98);
    }
  }
  v17 = (_QWORD *)sub_1407E58C0(&unk_141ABEC48, 24);
  v104 = v17;
  if ( qword_141ABE200 == 0 )
  {
    if ( dword_141B59AF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AF0);
      if ( dword_141B59AF0 == -1 )
      {
        sub_1407E5B40(&unk_141B59AB0);
        sub_141751048(sub_1407E6720);
        sub_141750EA0(&dword_141B59AF0);
        v17 = v104;
        v14 = a6;
        v15 = a5;
      }
    }
    qword_141ABE200 = (__int64)&unk_141B59AB0;
  }
  v17[2] = 0;
  v17[1] = 0;
  *v17 = 0;
  v18 = *(_DWORD *)v96;
  v100 = v18;
  v94 = 365 * a4;
  v83 = a9;
  v19 = HIWORD(v18);
  v20 = HIWORD(v18);
  v21 = v18;
  v99 = v18;
  while ( 1 )
  {
    v92 = v18;
    v27 = v18 & 0x1FF;
    v28 = v21 & 0x1FF;
    v29 = 365;
    v103 = v27;
    if ( (unsigned __int16)v20 <= (unsigned __int16)v19
      && ((unsigned __int16)v20 < (unsigned __int16)v19 || (unsigned __int16)v27 < v28) )
    {
      v29 = -365;
      v30 = v19;
      LOWORD(v19) = v20;
    }
    else
    {
      v30 = v20;
    }
    v93 = (unsigned __int16)v103;
    v31 = v29 * (v30 - (unsigned __int16)v19) + (unsigned __int16)v103 - v28;
    v32 = -v31;
    if ( v31 > 0 )
      v32 = v31;
    v97 = v20;
    v33 = a13;
    if ( v32 >= v94 )
      break;
    if ( v102 > 0 )
    {
      v34 = 0;
      while ( 1 )
      {
        v98 = v34;
        v35 = (_QWORD *)sub_140B49F70(v84, &v100, (unsigned int)v81[v34]);
        if ( v35 != nullptr )
        {
          v37 = v35;
          v38 = *v35;
          if ( v37[1] != v38 )
            break;
        }
LABEL_30:
        v34 = v98 + 1;
        LOWORD(v20) = v97;
        v17 = v104;
        if ( v98 + 1 >= v102 )
          goto LABEL_78;
      }
      v39 = 0;
      v89 = v37;
      while ( 2 )
      {
        v40 = *(_QWORD *)(v38 + 8 * v39);
        if ( v15 == 0
          || (LOBYTE(v36) = -1, (unsigned __int8)sub_140B53ED0(*(_QWORD *)(v38 + 8 * v39), v15, &v85, v36) != 0) )
        {
          if ( (v33 == 0 || *(_WORD *)(v40 + 48) == v33)
            && (v14 == 0 || *(_QWORD *)(v40 + 8) == v14 || *(_QWORD *)(v40 + 16) == v14) )
          {
            if ( a10 != 0 )
            {
LABEL_43:
              v41 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v40 + 272LL))(v40);
              v42 = v104;
              v43 = (__int64 *)v104[1];
              if ( v43 == (__int64 *)v104[2] )
              {
                v95 = v41;
                v48 = ((__int64)v43 - *v104) >> 3;
                v49 = v48 + (v48 >> 1);
                if ( v49 <= v48 + 1 )
                  v49 = v48 + 1;
                if ( v48 > 0x1FFFFFFFFFFFFFFFLL - (v48 >> 1) )
                  v49 = 0x1FFFFFFFFFFFFFFFLL;
                v50 = 8 * v49;
                v51 = *(_BYTE *)(qword_141ABE200 + 52) == 0;
                v82 = v48 + 1;
                v90 = 8 * v49;
                if ( v51
                  || (v52 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v52) >> 3 <= v50)
                  || (v53 = *(_QWORD *)(v52 + (v49 << 6))) == 0 )
                {
                  v54 = *(unsigned int *)(qword_141ABE200 + 48);
                  v55 = (char *)sub_141601260((unsigned int)(v54 + v50), 4096);
                }
                else
                {
                  v54 = *(unsigned int *)(v53 + 88);
                  v55 = (char *)sub_1407E58C0(v53, *(unsigned int *)(v53 + 80));
                }
                v56 = v55;
                if ( v54 != 0 )
                {
                  *(_DWORD *)v55 = v90;
                  v56 = &v55[v54];
                }
                *(_QWORD *)&v56[8 * v48] = v95;
                v42 = v104;
                v57 = (__int64 *)v104[1];
                sub_141758A00();
                if ( v57 != v43 )
                  sub_141758A00();
                if ( *v42 != 0 )
                  sub_1407E6420(qword_141ABE200, *v42, v42[2] - *v42);
                *v42 = v56;
                v44 = (__int64)&v56[8 * v82];
                v42[1] = v44;
                v42[2] = &v56[8 * v49];
                v14 = a6;
                v15 = a5;
                v33 = a13;
              }
              else
              {
                *v43 = v41;
                v44 = v42[1] + 8LL;
                v42[1] = v44;
              }
              v37 = v89;
              if ( a9 != -1 && (v44 - *v42) >> 3 >= v83 )
              {
                v98 = v102;
                goto LABEL_30;
              }
            }
            else
            {
              if ( a11 != 0 && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v40 + 240LL))(v40) == 0 )
              {
                v45 = *v104;
                v46 = (_QWORD *)v104[1];
                v47 = (_QWORD *)*v104;
                if ( (_QWORD *)*v104 != v46 )
                {
                  do
                  {
                    if ( *v47 != 0 )
                      (**(void (__fastcall ***)(_QWORD, __int64))*v47)(*v47, 1);
                    ++v47;
                  }
                  while ( v47 != v46 );
                  v58 = v104;
                  v59 = v104[1] - (_QWORD)v46;
                  sub_141758A00();
                  v58[1] = v45 + v59;
                }
                v39 = (__int64)(v37[1] - *v37) >> 3;
                v98 = v102;
                v15 = a5;
                v33 = a13;
                v14 = a6;
              }
              v60 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v40 + 240LL))(v40);
              if ( a8 != 0 )
              {
                if ( v60 != 0 )
                  goto LABEL_43;
              }
              else if ( v60 == 0 )
              {
                goto LABEL_43;
              }
            }
          }
        }
        ++v39;
        v38 = *v37;
        if ( v39 >= (__int64)(v37[1] - *v37) >> 3 )
          goto LABEL_30;
        continue;
      }
    }
LABEL_78:
    if ( a9 == -1 )
    {
      if ( v17[1] != *v17 )
        break;
    }
    else if ( a9 > 0 && (int)((v17[1] - *v17) >> 3) >= a9 )
    {
      break;
    }
    if ( a7 != 0 )
    {
      for ( i = v103; ; i += v62 )
      {
        v24 = (unsigned __int16)v20;
        v63 = 15;
        if ( (_WORD)v20 != 25
                         * (unsigned __int16)((((18351 * (unsigned int)(unsigned __int16)v20) >> 16)
                                             + ((unsigned __int16)(v20
                                                                 - ((18351 * (unsigned int)(unsigned __int16)v20) >> 16)) >> 1)) >> 4) )
          v63 = 3;
        if ( ((unsigned __int16)v20 & (unsigned __int16)v63) != 0 )
        {
          v62 = -365;
          if ( i < 365 )
          {
LABEL_91:
            v26 = (i + 1) & 0x1FF;
            goto LABEL_19;
          }
        }
        else
        {
          v62 = -366;
          if ( i < 366 )
            goto LABEL_91;
        }
        LOWORD(v20) = v20 + 1;
      }
    }
    v25 = v93 - 2;
    if ( (unsigned __int16)v103 < 2u )
    {
      v22 = v20 - 1;
      v23 = 3;
      if ( (unsigned __int16)(23593 * v22) < 0xA3Eu )
        v23 = 15;
      v24 = v22;
      LOWORD(v25) = ((unsigned __int16)(v22 & v23) == 0) + (_WORD)v25;
      v25 += 365;
    }
    else
    {
      v24 = (unsigned __int16)v20;
    }
    v26 = v25 + 1;
LABEL_19:
    v18 = v92 & 0xFFFFFE00 | v26;
    v99 = (v24 << 16) | (unsigned __int16)v18;
    v100 = v99;
    v21 = *v96;
    LOWORD(v19) = v96[1];
    v20 = v24;
  }
  if ( (v91 | v14) != 0 && a12 != 0 )
  {
    if ( qword_141ABE200 == 0 )
    {
      if ( dword_141B59AF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B59AF0);
        if ( dword_141B59AF0 == -1 )
        {
          sub_1407E5B40(&unk_141B59AB0);
          sub_141751048(sub_1407E6720);
          sub_141750EA0(&dword_141B59AF0);
          v17 = v104;
          LODWORD(v14) = a6;
          LOWORD(v20) = v97;
        }
      }
      qword_141ABE200 = (__int64)&unk_141B59AB0;
    }
    v87 = 0;
    v88 = 0;
    sub_140B55030((_DWORD)v96, v91, v14, a7, (__int64)&v87);
    v64 = v87;
    if ( (_QWORD)v87 == *((_QWORD *)&v87 + 1) )
    {
LABEL_121:
      if ( (_QWORD)v64 == 0 )
        goto LABEL_123;
      goto LABEL_122;
    }
    v65 = *(_QWORD *)v87;
    v66 = *(_WORD *)(*(_QWORD *)v87 + 78LL);
    v67 = *(_WORD *)(*(_QWORD *)v87 + 76LL) & 0x1FF;
    if ( a7 != 0 )
    {
      v68 = v103;
      if ( v66 < (unsigned __int16)v20 || v66 <= (unsigned __int16)v20 && v67 < (unsigned __int16)v103 )
      {
        v69 = *v17;
        v70 = (_QWORD *)v17[1];
        if ( (_QWORD *)*v17 != v70 )
        {
          v71 = (_QWORD *)*v17;
          do
          {
            if ( *v71 != 0 )
              (**(void (__fastcall ***)(_QWORD, __int64))*v71)(*v71, 1);
            ++v71;
          }
          while ( v71 != v70 );
LABEL_118:
          v17 = v104;
          v74 = v104[1] - (_QWORD)v70;
          sub_141758A00();
          v70 = (_QWORD *)(v69 + v74);
          v17[1] = v69 + v74;
LABEL_120:
          v99 = *(_DWORD *)(v65 + 76);
          v100 = v99;
          sub_140B57410(v17, v70, v64, (__int64)(*((_QWORD *)&v64 + 1) - v64) >> 3);
          goto LABEL_121;
        }
        goto LABEL_119;
      }
    }
    else
    {
      v68 = v103;
      if ( v66 > (unsigned __int16)v20 || v66 >= (unsigned __int16)v20 && v67 > (unsigned __int16)v103 )
      {
        v69 = *v17;
        v70 = (_QWORD *)v17[1];
        if ( (_QWORD *)*v17 != v70 )
        {
          v73 = (_QWORD *)*v17;
          do
          {
            if ( *v73 != 0 )
              (**(void (__fastcall ***)(_QWORD, __int64))*v73)(*v73, 1);
            ++v73;
          }
          while ( v73 != v70 );
          goto LABEL_118;
        }
LABEL_119:
        v17 = v104;
        goto LABEL_120;
      }
    }
    if ( v67 == v68 && v66 == (_WORD)v20 )
    {
      sub_140B57410(v17, v17[1], v87, (__int64)(*((_QWORD *)&v87 + 1) - v87) >> 3);
LABEL_122:
      sub_1407E6420(qword_141ABE200, v64, v88 - v64);
      goto LABEL_123;
    }
    v80 = (_QWORD *)v87;
    do
    {
      if ( *v80 != 0 )
        (**(void (__fastcall ***)(_QWORD, __int64))*v80)(*v80, 1);
      ++v80;
    }
    while ( v80 != *((_QWORD **)&v64 + 1) );
    v17 = v104;
    if ( (_QWORD)v64 != 0 )
      goto LABEL_122;
  }
LABEL_123:
  v75 = v17[1];
  if ( v75 == *v17 )
  {
    *v101 = 0;
    if ( v75 != 0 )
    {
      sub_1407E6420(qword_141ABE200, v75, v17[2] - v75);
      v17[2] = 0;
      v17[1] = 0;
      *v17 = 0;
    }
    sub_1409E5430(v17);
    result = v101;
  }
  else
  {
    *(_DWORD *)v96 = v99;
    result = v101;
    *v101 = v17;
  }
  if ( (_QWORD)v85 != 0 )
  {
    v76 = v86 - v85;
    if ( v86 - (_QWORD)v85 == -1 )
    {
      v76 = *(unsigned int *)(v85 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_137:
        MEMORY[0x141948990](v85 - *(unsigned int *)(qword_141ABD470 + 48));
        return v101;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_137;
    }
    v77 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v77) >> 3 <= v76 )
      goto LABEL_137;
    v78 = *(_QWORD *)(v77 + 8 * v76);
    if ( v78 == 0 )
      goto LABEL_137;
    MEMORY[0x1419475D8](v78 + 32, v85 - *(unsigned int *)(v78 + 120));
    v79 = *(_BYTE *)(v78 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v78 + 64)) != 0;
    result = v101;
    if ( !v79 && *(_BYTE *)(v78 + 97) != 0 )
    {
      sub_1412D33C0(v78);
      return v101;
    }
  }
  return result;
}
