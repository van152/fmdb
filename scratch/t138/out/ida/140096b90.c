__int64 __fastcall sub_140096B90(_QWORD *a1, int a2)
{
  unsigned __int64 v2; // r14
  volatile signed __int32 *v5; // rax
  __int64 v6; // rdx
  _QWORD *v7; // rdi
  bool v8; // cf
  int v9; // esi
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  int v11; // esi
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  int v13; // ebx
  __int64 v14; // rdx
  __int64 v15; // rsi
  void (__fastcall ***v16)(_QWORD, __int64); // rcx
  int v17; // esi
  void (__fastcall ***v18)(_QWORD, __int64); // rcx
  int v19; // esi
  void (__fastcall ***v20)(_QWORD, __int64); // rcx
  int v21; // esi
  void (__fastcall ***v22)(_QWORD, __int64); // rcx
  int v23; // esi
  void (__fastcall ***v24)(_QWORD, __int64); // rcx
  int v25; // esi
  void (__fastcall ***v26)(_QWORD, __int64); // rcx
  __int64 *v27; // rdi
  __int64 *v28; // rsi
  unsigned __int16 v29; // ax
  int v30; // esi
  void (__fastcall ***v31)(_QWORD, __int64); // rcx
  _QWORD *v32; // r8
  int v33; // esi
  void (__fastcall ***v34)(_QWORD, __int64); // rcx
  _QWORD *v35; // r15
  _QWORD *v36; // rbp
  _QWORD *v37; // rbx
  volatile signed __int32 *v38; // rbx
  __int64 v39; // rbp
  volatile signed __int32 *v40; // rbp
  char v41; // al
  char v42; // bl
  void (__fastcall ***v43)(_QWORD, __int64); // rcx
  volatile signed __int32 *v44; // rsi
  int v45; // r12d
  __int64 v46; // r15
  _QWORD *v47; // rbp
  char v48; // r13
  volatile signed __int32 *v49; // rcx
  __int64 v50; // rbp
  unsigned __int64 v51; // rdi
  unsigned __int64 v52; // rbx
  unsigned __int64 v53; // rcx
  unsigned __int64 v54; // rbx
  __int64 v55; // rsi
  unsigned __int64 *v56; // rsi
  _QWORD *v57; // rdi
  _QWORD *v58; // rbx
  unsigned __int64 v59; // rbp
  _QWORD *v60; // rsi
  volatile signed __int32 *v61; // rsi
  __int64 v62; // rsi
  char v63; // bl
  void (__fastcall ***v64)(_QWORD, __int64); // rcx
  __int64 *v65; // rbx
  __int64 *v66; // rbp
  __int64 v67; // rdi
  unsigned __int64 v68; // rax
  unsigned __int64 v69; // r12
  unsigned __int64 v70; // rcx
  unsigned __int64 v71; // r12
  __int64 v72; // r13
  __int64 *v73; // rsi
  volatile signed __int32 *v74; // rsi
  __int64 *v75; // rbx
  __int64 v76; // rbp
  __int64 v77; // rbp
  volatile signed __int32 *v78; // rcx
  volatile signed __int32 *v80; // [rsp+48h] [rbp-B0h] BYREF
  volatile signed __int32 *v81; // [rsp+50h] [rbp-A8h] BYREF
  volatile signed __int32 *v82; // [rsp+58h] [rbp-A0h] BYREF
  __int128 v83; // [rsp+60h] [rbp-98h] BYREF
  __int64 v84; // [rsp+70h] [rbp-88h]
  _QWORD *v85; // [rsp+78h] [rbp-80h]
  _BYTE v86[4]; // [rsp+80h] [rbp-78h] BYREF
  unsigned __int16 v87; // [rsp+84h] [rbp-74h]
  int v88; // [rsp+8Ch] [rbp-6Ch] BYREF
  __int128 v89; // [rsp+90h] [rbp-68h] BYREF
  __int64 v90; // [rsp+A0h] [rbp-58h]
  volatile signed __int32 *v91; // [rsp+B0h] [rbp-48h] BYREF

  sub_1407D0D60(a1: v86);
  sub_1407D0F70(
    a1: (unsigned int)v86,
    a2: (unsigned int)&v81,
    a3: a2,
    a4: (unsigned int)&unk_141ABEA68,
    a5: (__int64)&unk_141B59880,
    a6: 0,
    a7: 0,
    a8: 0);
  v5 = v81;
  if ( v81 == nullptr )
  {
    LODWORD(v2) = 0;
    return (unsigned int)v2;
  }
  *((_WORD *)a1 + 846) = v87;
  *((_BYTE *)a1 + 392) = 1;
  v91 = v5;
  _InterlockedIncrement(v5 + 2);
  if ( (unsigned __int8)sub_140079270(a1: &v91) != 0 )
  {
    if ( qword_141ABD470 == 0 )
      qword_141ABD470 = sub_1407E4940();
    v89 = 0;
    v90 = 0;
    sub_140054B60(a1: &v89, a2: 0, a3: a1[89], a4: (__int64)(a1[90] - a1[89]) >> 3);
    v6 = a1[89];
    if ( v6 != a1[90] )
      a1[90] = v6;
    v7 = a1 + 89;
    v8 = *((_WORD *)a1 + 846) < 7u;
    v85 = a1;
    if ( !v8 )
    {
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      sub_14007B6D0(a1: &v80, a2: &v83, a3: a1 + 103, a4: &v82);
      v9 = (int)v80;
      v10 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v10)(a1: v10, a2: 1);
      if ( v9 != 0 )
        goto LABEL_65;
      if ( v87 >= 2u )
      {
        *(_QWORD *)&v83 = v81;
        if ( v81 != nullptr )
          _InterlockedIncrement(v81 + 2);
        sub_14007B6D0(a1: &v80, a2: &v83, a3: a1 + 107, a4: &v82);
        v11 = (int)v80;
        v12 = (void (__fastcall ***)(_QWORD, __int64))v83;
        if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
          (**v12)(a1: v12, a2: 1);
        if ( v11 != 0 )
          goto LABEL_65;
      }
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      if ( a1[112] == a1[111] )
      {
        LODWORD(v80) = 0;
        (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, __int64))(*(_QWORD *)v83 + 40LL))(
          a1: v83,
          a2: &v80,
          a3: 4);
        v13 = 1;
        if ( qword_141AA7808 > (unsigned __int64)(unsigned int)v80 )
        {
          sub_14007B930(a1: a1 + 111);
          v14 = a1[111];
          if ( (a1[112] - v14) >> 2 >= (unsigned __int64)(unsigned int)v80 )
          {
            v15 = v83;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v83 + 40LL))(
              a1: v83,
              a2: v14,
              a3: 4LL * (unsigned int)v80);
            v13 = *(_DWORD *)(v15 + 16);
          }
        }
        LODWORD(v82) = v13;
      }
      else
      {
        sub_14007BA50(a1: &v82, a2: &v83, a3: a1 + 111, a4: &v80);
        v13 = (int)v82;
      }
      v16 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v16)(a1: v16, a2: 1);
      if ( v13 != 0 )
        goto LABEL_65;
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      sub_14007BC80(a1: &v80, a2: &v83, a3: a1 + 80, a4: &v82);
      v17 = (int)v80;
      v18 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v18)(a1: v18, a2: 1);
      if ( v17 != 0 )
        goto LABEL_65;
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      sub_14007BF10(a1: &v80, a2: &v83, a3: a1 + 86, a4: &v82);
      v19 = (int)v80;
      v20 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v20)(a1: v20, a2: 1);
      if ( v19 != 0 )
        goto LABEL_65;
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      sub_14007C3B0(a1: &v80, a2: &v83, a3: a1 + 89, a4: &v82);
      v21 = (int)v80;
      v22 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v22)(a1: v22, a2: 1);
      if ( v21 != 0 )
        goto LABEL_65;
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      sub_14007C3B0(a1: &v80, a2: &v83, a3: a1 + 97, a4: &v82);
      v23 = (int)v80;
      v24 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v24)(a1: v24, a2: 1);
      if ( v23 != 0 )
        goto LABEL_65;
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      sub_14007C7C0(a1: &v80, a2: &v83, a3: a1 + 76, a4: &v82);
      v25 = (int)v80;
      v26 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v26)(a1: v26, a2: 1);
      if ( v25 != 0 )
        goto LABEL_65;
      *((_BYTE *)a1 + 632) = 0;
      v29 = v87;
      if ( v87 <= 2u )
      {
        if ( qword_141ABD470 == 0 )
          qword_141ABD470 = sub_1407E4940();
        v83 = 0;
        v84 = 0;
        v80 = v81;
        if ( v81 != nullptr )
          _InterlockedIncrement(v81 + 2);
        sub_14007A6C0(a1: &v82, a2: &v80, a3: &v83);
        v30 = (int)v82;
        v31 = (void (__fastcall ***)(_QWORD, __int64))v80;
        if ( v80 != nullptr && _InterlockedDecrement(v80 + 2) == 0 )
          (**v31)(a1: v31, a2: 1);
        if ( (_QWORD)v83 != 0 )
          sub_1407E4890(a1: qword_141ABD470);
        if ( v30 != 0 )
          goto LABEL_65;
        v29 = v87;
      }
      if ( v29 >= 4u )
      {
        v32 = v85 + 114;
        *(_QWORD *)&v83 = v81;
        if ( v81 != nullptr )
          _InterlockedIncrement(v81 + 2);
        sub_14007A760(a1: &v80, a2: &v83, a3: v32);
        v33 = (int)v80;
        v34 = (void (__fastcall ***)(_QWORD, __int64))v83;
        if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
          (**v34)(a1: v34, a2: 1);
        if ( v33 != 0 )
          goto LABEL_65;
      }
      v35 = v85;
      v36 = (_QWORD *)v85[97];
      v37 = (_QWORD *)v85[98];
      if ( v36 != v37 )
      {
        v2 = (unsigned __int64)&v83;
        do
        {
          *(_QWORD *)&v83 = *v36;
          if ( *(_DWORD *)(v83 + 24) == 27 )
            sub_14002DCA0(a1: v35 + 92, a2: &v83);
          ++v36;
        }
        while ( v36 != v37 );
      }
      sub_14007A8A0(a1: v35 + 100);
      v38 = v81;
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v81 + 40LL))(
        a1: v81,
        a2: &v80,
        a3: 4);
      if ( *((_DWORD *)v38 + 4) == 0 && (_DWORD)v80 != -1 )
      {
        v2 = (unsigned __int64)&v83;
        do
        {
          v39 = sub_14007A910(a1: 24);
          sub_1407C9510(a1: v39);
          *(_QWORD *)&v83 = v39;
          sub_140839480(a1: v81, a2: &v82, a3: v39);
          if ( (_DWORD)v82 != 0 )
            goto LABEL_65;
          sub_14007A9C0(a1: v35 + 100, a2: &v83, a3: (int)v80);
          v40 = v81;
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v81 + 40LL))(
            a1: v81,
            a2: &v80,
            a3: 4);
        }
        while ( *((_DWORD *)v40 + 4) == 0 && (_DWORD)v80 != -1 );
      }
      a1 = v85;
      v6 = v85[90];
    }
    sub_140054B60(a1: v7, a2: v6, a3: v89, a4: (__int64)(*((_QWORD *)&v89 + 1) - v89) >> 3);
    if ( (_QWORD)v89 != *((_QWORD *)&v89 + 1) )
      *((_QWORD *)&v89 + 1) = v89;
    if ( v87 <= 5u )
    {
      while ( 1 )
      {
        v80 = v81;
        if ( v81 != nullptr )
          _InterlockedIncrement(v81 + 2);
        v41 = sub_140FCBFB0(a1: &v83, a2: &v80);
        v42 = v41 & ((_QWORD)v83 != 0);
        v43 = (void (__fastcall ***)(_QWORD, __int64))v80;
        if ( v80 != nullptr && _InterlockedDecrement(v80 + 2) == 0 )
          (**v43)(a1: v43, a2: 1);
        if ( v42 == 0 )
          break;
        if ( qword_141ABD470 == 0 )
          qword_141ABD470 = sub_1407E4940();
        v44 = v81;
        (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v81 + 40LL))(
          a1: v81,
          a2: &v88,
          a3: 4);
        if ( *((_DWORD *)v44 + 4) == 0 )
        {
          if ( v88 <= 0 )
            continue;
          v45 = 0;
          v46 = 0;
          v47 = nullptr;
          v2 = 0;
          while ( 1 )
          {
            v82 = v81;
            if ( v81 != nullptr )
              _InterlockedIncrement(v81 + 2);
            v48 = sub_140FCBF10(a1: &v80, a2: &v82);
            v49 = v82;
            if ( v82 != nullptr && _InterlockedDecrement(v82 + 2) == 0 )
              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v49)(a1: v49, a2: 1);
            if ( v48 == 0 )
              break;
            if ( v47 == (_QWORD *)v2 )
            {
              v50 = (__int64)v47 - v46;
              v51 = (v50 >> 3) + 1;
              v52 = (unsigned __int64)(v50 >> 3) >> 1;
              v53 = 0x1FFFFFFFFFFFFFFFLL - v52;
              v54 = (v50 >> 3) + v52;
              if ( v54 <= v51 )
                v54 = (v50 >> 3) + 1;
              if ( v50 >> 3 > v53 )
                v54 = 0x1FFFFFFFFFFFFFFFLL;
              v55 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v54);
              *(_QWORD *)(v55 + v50) = v80;
              sub_141758A00(a1: v55, a2: v46, a3: v50);
              if ( v46 != 0 )
                sub_1407E4890(a1: qword_141ABD470);
              v47 = (_QWORD *)(v55 + 8 * v51);
              v2 = v55 + 8 * v54;
              v46 = v55;
              if ( ++v45 >= v88 )
                break;
            }
            else
            {
              *v47++ = v80;
              if ( ++v45 >= v88 )
                break;
            }
          }
          if ( v46 != 0 )
          {
            LODWORD(v2) = v2 - v46;
            sub_1407E4890(a1: qword_141ABD470);
          }
          a1 = v85;
          if ( v48 != 0 )
            continue;
        }
        goto LABEL_65;
      }
    }
    v56 = (unsigned __int64 *)a1[47];
    if ( v56 != nullptr )
    {
      v2 = *v56;
      v57 = (_QWORD *)v56[1];
      if ( (_QWORD *)*v56 != v57 )
      {
        v58 = (_QWORD *)*v56;
        do
        {
          if ( *v58 != 0 )
            (**(void (__fastcall ***)(_QWORD, __int64))*v58)(a1: *v58, a2: 1);
          ++v58;
        }
        while ( v58 != v57 );
        v59 = v56[1] - (_QWORD)v57;
        sub_141758A00(a1: v2, a2: v57, a3: v59);
        v56[1] = v2 + v59;
        v57 = (_QWORD *)*v56;
      }
      if ( v57 != nullptr )
      {
        sub_1407E6420(a1: qword_141ABE200, a2: v57, a3: v56[2] - (_QWORD)v57);
        v56[2] = 0;
        v56[1] = 0;
        *v56 = 0;
      }
      sub_1400940B0(a1: v56);
    }
    a1[47] = 0;
    v60 = (_QWORD *)sub_140098A00(a1: 24);
    if ( qword_141ABE200 == 0 )
      qword_141ABE200 = sub_1407E6540();
    v60[2] = 0;
    v60[1] = 0;
    *v60 = 0;
    a1[47] = v60;
    v61 = v81;
    (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v81 + 40LL))(
      a1: v81,
      a2: &v80,
      a3: 1);
    if ( *((_DWORD *)v61 + 4) != 0 || ((unsigned __int8)v80 & 1) == 0 )
    {
LABEL_164:
      *((_WORD *)a1 + 846) = 10;
      LOBYTE(v2) = 1;
      v27 = *((__int64 **)&v89 + 1);
      v28 = (__int64 *)v89;
      if ( (_QWORD)v89 == *((_QWORD *)&v89 + 1) )
        goto LABEL_170;
      goto LABEL_165;
    }
    while ( 1 )
    {
      v62 = sub_14003DB70(a1: 88);
      sub_140B22770(a1: v62);
      *(_QWORD *)&v83 = v81;
      if ( v81 != nullptr )
        _InterlockedIncrement(v81 + 2);
      v63 = (*(__int64 (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v62 + 264LL))(a1: v62, a2: &v83);
      v64 = (void (__fastcall ***)(_QWORD, __int64))v83;
      if ( (_QWORD)v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 8)) == 0 )
        (**v64)(a1: v64, a2: 1);
      if ( v63 == 0 )
        break;
      v65 = (__int64 *)a1[47];
      v66 = (__int64 *)v65[1];
      if ( v66 == (__int64 *)v65[2] )
      {
        v67 = (__int64)v66 - *v65;
        v68 = v67 >> 3;
        v2 = (v67 >> 3) + 1;
        v69 = (unsigned __int64)(v67 >> 3) >> 1;
        v70 = 0x1FFFFFFFFFFFFFFFLL - v69;
        v71 = (v67 >> 3) + v69;
        if ( v71 <= v2 )
          v71 = v68 + 1;
        if ( v68 > v70 )
          v71 = 0x1FFFFFFFFFFFFFFFLL;
        v72 = sub_1407E6360(a1: qword_141ABE200, a2: 8 * v71);
        *(_QWORD *)(v72 + v67) = v62;
        v73 = (__int64 *)v65[1];
        sub_141758A00(a1: v72, a2: *v65, a3: (char *)v66 - *v65);
        if ( v73 != v66 )
          sub_141758A00(a1: v72 + v67 + 8, a2: v66, a3: v65[1] - (_QWORD)v66);
        if ( *v65 != 0 )
          sub_1407E6420(a1: qword_141ABE200, a2: *v65, a3: v65[2] - *v65);
        *v65 = v72;
        v65[1] = v72 + 8 * v2;
        v65[2] = v72 + 8 * v71;
        a1 = v85;
      }
      else
      {
        *v66 = v62;
        v65[1] += 8;
      }
      v74 = v81;
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v81 + 40LL))(
        a1: v81,
        a2: &v80,
        a3: 1);
      if ( *((_DWORD *)v74 + 4) != 0 || ((unsigned __int8)v80 & 1) == 0 )
        goto LABEL_164;
    }
LABEL_65:
    LODWORD(v2) = 0;
    v27 = *((__int64 **)&v89 + 1);
    v28 = (__int64 *)v89;
    if ( (_QWORD)v89 == *((_QWORD *)&v89 + 1) )
    {
LABEL_170:
      if ( v27 != nullptr )
        sub_1407E4890(a1: qword_141ABD470);
      goto LABEL_172;
    }
LABEL_165:
    v75 = v28;
    do
    {
      v76 = *v75;
      if ( *v75 != 0 )
      {
        sub_140808B00(a1: v76 + 32);
        sub_14007C700(a1: v76);
      }
      ++v75;
    }
    while ( v75 != v27 );
    v77 = *((_QWORD *)&v89 + 1) - (_QWORD)v27;
    sub_141758A00(a1: v28, a2: v27, a3: *((_QWORD *)&v89 + 1) - (_QWORD)v27);
    *((_QWORD *)&v89 + 1) = (char *)v28 + v77;
    v27 = (__int64 *)v89;
    goto LABEL_170;
  }
  LODWORD(v2) = 0;
LABEL_172:
  v78 = v81;
  if ( v81 != nullptr && _InterlockedDecrement(v81 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v78)(a1: v78, a2: 1);
  return (unsigned int)v2;
}
