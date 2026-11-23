__int64 __fastcall sub_140F51450(__int64 *a1, __int64 a2, unsigned int a3, char a4, char a5)
{
  __int64 v9; // rbp
  __int64 v10; // rcx
  volatile signed __int32 *v11; // rcx
  __int64 v12; // rax
  unsigned int v13; // ecx
  __int64 v14; // r9
  void (__fastcall ***v15)(_QWORD, __int64); // rcx
  __int64 v16; // rbp
  char v17; // bl
  void (__fastcall ***v18)(_QWORD, __int64); // rcx
  void (__fastcall ***v19)(_QWORD, __int64); // rcx
  __int64 v20; // rcx
  __int64 v21; // rsi
  void (__fastcall ***v22)(_QWORD, __int64); // rcx
  __int64 v23; // rcx
  __int64 v25; // r12
  __int64 **v26; // rax
  __int64 *v27; // rbp
  __int64 *v28; // rsi
  __int64 v29; // rax
  __int64 v30; // rdi
  unsigned int v31; // ebx
  __int64 v32; // rax
  int v33; // edx
  char v34; // al
  __int64 v35; // rbp
  char v36; // r12
  void (__fastcall ***v37)(_QWORD, __int64); // rcx
  void (__fastcall ***v38)(_QWORD, __int64); // rcx
  __int64 v39; // rcx
  __int64 v40; // rax
  _QWORD *v41; // rdi
  _QWORD *v42; // rbx
  char v43; // r12
  char v44; // al
  char v45; // cl
  __int64 v46; // rbp
  char v47; // r12
  void (__fastcall ***v48)(_QWORD, __int64); // rcx
  void (__fastcall ***v49)(_QWORD, __int64); // rcx
  __int64 v50; // rcx
  bool v51; // zf
  __int64 v52; // rdx
  __int64 v53; // rcx
  __int64 v54; // r8
  __int64 v55; // r9
  char v56; // cl
  char v57; // dl
  char v58; // cl
  char v59; // dl
  char v60; // cl
  char v61; // dl
  void (__fastcall ***v62)(_QWORD, __int64); // rcx
  int v63; // [rsp+20h] [rbp-A8h]
  __int64 v64; // [rsp+40h] [rbp-88h] BYREF
  char v65; // [rsp+4Fh] [rbp-79h]
  __int64 v66; // [rsp+50h] [rbp-78h] BYREF
  __int64 v67; // [rsp+58h] [rbp-70h] BYREF
  __int64 v68; // [rsp+60h] [rbp-68h] BYREF
  __int64 v69; // [rsp+68h] [rbp-60h] BYREF
  __int64 v70; // [rsp+70h] [rbp-58h] BYREF
  __int64 v71; // [rsp+78h] [rbp-50h] BYREF
  _BYTE v72[72]; // [rsp+80h] [rbp-48h] BYREF

  v69 = 0;
  v9 = sub_1412EC810(a1: 264, a2: 9);
  *(_QWORD *)v9 = 0x900000000LL;
  if ( (_BYTE)a3 != 0 )
    v10 = 0x645F726576726573LL;
  else
    v10 = 0x645F746E65696C63LL;
  *(_QWORD *)(v9 + 8) = v10;
  *(_BYTE *)(v9 + 16) = 98;
  *(_BYTE *)(v9 + 17) = 0;
  _InterlockedIncrement((volatile signed __int32 *)v9);
  _InterlockedIncrement((volatile signed __int32 *)v9);
  if ( v69 == v9 + 4 )
  {
    if ( _InterlockedDecrement((volatile signed __int32 *)v9) == 0 )
      sub_1412EC9A0(a1: v9);
  }
  else
  {
    v11 = (volatile signed __int32 *)(v69 - 4);
    if ( v69 != 0 && _InterlockedDecrement(v11) == 0 )
      sub_1412EC9A0(a1: v11);
    v69 = v9 + 4;
  }
  if ( _InterlockedDecrement((volatile signed __int32 *)v9) == 0 )
    sub_1412EC9A0(a1: v9);
  v71 = 0x80100004E554C4CLL;
  sub_14080D0E0(a1: &v66, a2: 0x1418E2C24LL);
  sub_1407D0F70(
    a1: (unsigned int)&v71,
    a2: (unsigned int)&v70,
    a3: a2,
    a4: (unsigned int)&v69,
    a5: (__int64)&v66,
    a6: 0,
    a7: 0);
  v12 = v70;
  if ( v70 == 0 )
  {
    sub_140F2B090();
    LODWORD(v21) = 0;
    goto LABEL_34;
  }
  v13 = WORD2(v71);
  *((_WORD *)a1 + 708) = WORD2(v71);
  if ( v13 <= 0xDF1 )
  {
    v66 = v12;
    _InterlockedIncrement((volatile signed __int32 *)(v12 + 8));
    sub_1407C5A20(a1: &v64, a2: &v66, a3: a2, a4: &v69);
    v15 = (void (__fastcall ***)(_QWORD, __int64))v66;
    if ( v66 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v66 + 8)) == 0 )
      (**v15)(a1: v15, a2: 1);
    if ( v64 != 0 )
    {
      LOBYTE(v14) = 1;
      if ( (unsigned __int8)sub_140F4EEB0(a1, a2: &v64, a3, a4: v14) == 0 )
        goto LABEL_150;
      v65 = a4;
      *((_BYTE *)a1 + 1450) = 1;
      v16 = *a1;
      v67 = 0;
      if ( (*(_BYTE *)(v16 + 92) & 2) != 0 )
      {
        *(_BYTE *)(v16 + 89) = 1;
      }
      else
      {
        sub_14080D0E0(a1: v72, a2: 0x1418E2C24LL);
        v17 = 0;
        sub_140FFADB0(a1: v16, a2: &v67, a3: 0, a4: 0);
        v66 = 0x80100004E554C4CLL;
        sub_1407D0F70(
          a1: (unsigned int)&v66,
          a2: (unsigned int)&v68,
          a3: (unsigned int)&v64,
          a4: (unsigned int)&v67,
          a5: (__int64)v72,
          a6: 0,
          a7: 0);
        if ( v68 != 0 )
        {
          v66 = v68;
          _InterlockedIncrement((volatile signed __int32 *)(v68 + 8));
          v17 = sub_140F2B6D0(a1: v16, a2: &v66, a3: a1, a4: a3);
          v18 = (void (__fastcall ***)(_QWORD, __int64))v66;
          if ( v66 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v66 + 8)) == 0 )
            (**v18)(a1: v18, a2: 1);
          v19 = (void (__fastcall ***)(_QWORD, __int64))v68;
          if ( v68 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v68 + 8)) == 0 )
            (**v19)(a1: v19, a2: 1);
        }
        v20 = v67;
        if ( v67 == 0 || _InterlockedDecrement((volatile signed __int32 *)(v67 - 4)) != 0 )
        {
          if ( v17 == 0 )
            goto LABEL_150;
        }
        else
        {
          sub_1412EC9A0(a1: v20 - 4);
          if ( v17 == 0 )
            goto LABEL_150;
        }
      }
      v25 = *a1;
      v26 = *(__int64 ***)(*a1 + 128);
      v27 = *v26;
      v28 = v26[1];
      v29 = *a1;
      if ( v27 != v28 )
      {
        do
        {
          v30 = *v27;
          if ( *v27 != 0 )
          {
            v31 = *(unsigned __int8 *)(v25 + 90);
            sub_140F7F220(a1, a2: v30 + 80, a3: *(unsigned __int8 *)(v25 + 90));
            sub_140F7FA30(a1, a2: v30 + 96, a3: v31, a4: 0);
            sub_140F7F010(a1, a2: v30 + 88, a3: v31, a4: 0);
            sub_140F7F730(a1, a2: v30 + 104, a3: v31);
            v32 = *(_QWORD *)(v30 + 88);
            if ( v32 != 0 && *(_DWORD *)(v32 + 12) == 100000023 )
            {
              *(_BYTE *)(v30 + 131) = 6;
              if ( *(_BYTE *)(v30 + 137) == 8 )
                *(_BYTE *)(v30 + 137) = 7;
            }
          }
          ++v27;
        }
        while ( v27 != v28 );
        v29 = *a1;
      }
      v33 = *(_BYTE *)(a1[12] + 89) | 2;
      if ( *(_BYTE *)(v29 + 89) == 0 )
        v33 = *(unsigned __int8 *)(a1[12] + 89);
      v34 = v33 | 4;
      if ( *(_BYTE *)(a1[13] + 89) == 0 )
        v34 = v33;
      *(_BYTE *)(v25 + 90) = v34;
      v35 = a1[9];
      v67 = 0;
      if ( (*(_BYTE *)(v35 + 92) & 2) != 0 )
      {
        *(_BYTE *)(v35 + 89) = 1;
      }
      else
      {
        sub_14080D0E0(a1: v72, a2: 0x1418E2C24LL);
        v36 = 0;
        sub_140FFADB0(a1: v35, a2: &v67, a3: 0, a4: 0);
        v66 = 0x80100004E554C4CLL;
        sub_1407D0F70(
          a1: (unsigned int)&v66,
          a2: (unsigned int)&v68,
          a3: (unsigned int)&v64,
          a4: (unsigned int)&v67,
          a5: (__int64)v72,
          a6: 0,
          a7: 0);
        if ( v68 != 0 )
        {
          v66 = v68;
          _InterlockedIncrement((volatile signed __int32 *)(v68 + 8));
          v36 = sub_140F2D3A0(a1: v35, a2: &v66, a3: a1, a4: a3);
          v37 = (void (__fastcall ***)(_QWORD, __int64))v66;
          if ( v66 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v66 + 8)) == 0 )
            (**v37)(a1: v37, a2: 1);
          v38 = (void (__fastcall ***)(_QWORD, __int64))v68;
          if ( v68 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v68 + 8)) == 0 )
            (**v38)(a1: v38, a2: 1);
        }
        v39 = v67;
        if ( v67 == 0 || _InterlockedDecrement((volatile signed __int32 *)(v67 - 4)) != 0 )
        {
          if ( v36 == 0 )
            goto LABEL_150;
        }
        else
        {
          sub_1412EC9A0(a1: v39 - 4);
          if ( v36 == 0 )
            goto LABEL_150;
        }
      }
      v21 = a1[9];
      v40 = *(_QWORD *)(v21 + 128);
      v41 = *(_QWORD **)v40;
      v42 = *(_QWORD **)(v40 + 8);
      v43 = v65;
      if ( *(_QWORD **)v40 != v42 )
      {
        do
        {
          if ( *v41 != 0 )
          {
            LOBYTE(v33) = 1;
            sub_141546980(a1: *v41, a2: v33, a3: (_DWORD)a1, a4: a3, a5: *(_BYTE *)(v21 + 90));
          }
          ++v41;
        }
        while ( v41 != v42 );
      }
      v44 = *(_BYTE *)(a1[12] + 89) | 2;
      if ( *(_BYTE *)(*a1 + 89) == 0 )
        v44 = *(_BYTE *)(a1[12] + 89);
      v45 = v44 | 4;
      if ( *(_BYTE *)(a1[13] + 89) == 0 )
        v45 = v44;
      *(_BYTE *)(v21 + 90) = v45;
      v46 = a1[14];
      v67 = 0;
      if ( (*(_BYTE *)(v46 + 92) & 2) != 0 )
      {
        *(_BYTE *)(v46 + 89) = 1;
      }
      else
      {
        sub_14080D0E0(a1: v72, a2: 0x1418E2C24LL);
        v47 = 0;
        sub_140FFADB0(a1: v46, a2: &v67, a3: 0, a4: 0);
        v66 = 0x80100004E554C4CLL;
        sub_1407D0F70(
          a1: (unsigned int)&v66,
          a2: (unsigned int)&v68,
          a3: (unsigned int)&v64,
          a4: (unsigned int)&v67,
          a5: (__int64)v72,
          a6: 0,
          a7: 0);
        if ( v68 != 0 )
        {
          v66 = v68;
          _InterlockedIncrement((volatile signed __int32 *)(v68 + 8));
          v47 = sub_140F30650(a1: v46, a2: &v66, a3: a1, a4: a3);
          v48 = (void (__fastcall ***)(_QWORD, __int64))v66;
          if ( v66 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v66 + 8)) == 0 )
            (**v48)(a1: v48, a2: 1);
          v49 = (void (__fastcall ***)(_QWORD, __int64))v68;
          if ( v68 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v68 + 8)) == 0 )
            (**v49)(a1: v49, a2: 1);
        }
        v50 = v67;
        if ( v67 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v67 - 4)) == 0 )
          sub_1412EC9A0(a1: v50 - 4);
        v51 = v47 == 0;
        v43 = v65;
        if ( v51 )
          goto LABEL_150;
      }
      if ( (unsigned __int8)sub_140F52140(a1: a1[8], a2: &v64, a3: a1, a4: a3) == 0
        || (unsigned __int8)sub_140F52270(a1: a1[22], a2: &v64, a3: a1, a4: a3) == 0 )
      {
        goto LABEL_150;
      }
      sub_140F4B330(a1: a1[22], a2: a1, a3);
      if ( (_BYTE)a3 == 0 )
        goto LABEL_145;
      if ( (unsigned __int8)sub_140F523A0(a1: a1[110], a2: &v64, a3: a1) == 0 )
      {
LABEL_150:
        LODWORD(v21) = 0;
        goto LABEL_151;
      }
      sub_140F4B620(a1: a1[110], a2: a1);
      if ( v43 != 0 )
      {
        if ( a5 != 0 )
        {
          if ( (unsigned __int8)sub_140F524C0(a1: a1[105], a2: &v64, a3: a1) == 0 )
            goto LABEL_150;
          sub_140F4B3D0(a1: a1[105], a2: a1);
          if ( (unsigned __int8)sub_140F52A80(a1: a1[107], a2: &v64, a3: a1) == 0 )
            goto LABEL_150;
          sub_140F4B4E0(a1: a1[107], a2: a1);
          if ( (unsigned __int8)sub_140F52BA0(a1: a1[117], a2: &v64, a3: a1) == 0 )
            goto LABEL_150;
          sub_140F4B760(a1: a1[117], a2: a1);
          if ( (unsigned __int8)sub_140F52CC0(a1: a1[120], a2: &v64, a3: a1) == 0 )
            goto LABEL_150;
          sub_140F4B590(a1: a1[120], a2: a1);
          if ( (unsigned __int8)sub_140F52DE0(a1: a1[122], a2: &v64, a3: a1) == 0
            || (unsigned __int8)sub_140F52F00(a1: a1[124], a2: &v64, a3: a1) == 0
            || (unsigned __int8)sub_140F53020(a1: a1[130], a2: &v64, a3: a1) == 0 )
          {
            goto LABEL_150;
          }
          v56 = *(_BYTE *)(a1[12] + 89) | 2;
          if ( *(_BYTE *)(*a1 + 89) == 0 )
            v56 = *(_BYTE *)(a1[12] + 89);
          v57 = v56 | 4;
          if ( *(_BYTE *)(a1[13] + 89) == 0 )
            v57 = v56;
          *(_BYTE *)(a1[130] + 90) = v57;
          if ( (unsigned __int8)sub_140F53140(a1: a1[135], a2: &v64, a3: a1) == 0 )
            goto LABEL_150;
          sub_140F4BB20(a1: a1[135], a2: a1);
          if ( (unsigned __int8)sub_140F53260(a1: a1[115], a2: &v64, a3: a1) == 0 )
            goto LABEL_150;
          sub_140F4B6D0(a1: a1[115], a2: a1);
          if ( (unsigned __int8)sub_140F537D0(a1: a1[123], a2: &v64, a3: a1) == 0
            || (unsigned __int8)sub_140F538F0(a1: a1[131], a2: &v64, a3: a1) == 0 )
          {
            goto LABEL_150;
          }
        }
        if ( (unsigned __int8)sub_140F53A10(a1: a1[111], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F53A10(a1: a1[112], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F53A10(a1: a1[113], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F53A10(a1: a1[114], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F53F80(a1: a1[116], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F544F0(a1: a1[108], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        sub_140F4B590(a1: a1[108], a2: a1);
        if ( (unsigned __int8)sub_140F54610(a1: a1[121], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        sub_140F4B9D0(a1: a1[121], a2: a1);
        if ( (unsigned __int8)sub_140F54730(a1: a1[125], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        v58 = *(_BYTE *)(a1[12] + 89) | 2;
        if ( *(_BYTE *)(*a1 + 89) == 0 )
          v58 = *(_BYTE *)(a1[12] + 89);
        v59 = v58 | 4;
        if ( *(_BYTE *)(a1[13] + 89) == 0 )
          v59 = v58;
        *(_BYTE *)(a1[125] + 90) = v59;
        if ( (unsigned __int8)sub_140F54730(a1: a1[126], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        v60 = *(_BYTE *)(a1[12] + 89) | 2;
        if ( *(_BYTE *)(*a1 + 89) == 0 )
          v60 = *(_BYTE *)(a1[12] + 89);
        v61 = v60 | 4;
        if ( *(_BYTE *)(a1[13] + 89) == 0 )
          v61 = v60;
        *(_BYTE *)(a1[126] + 90) = v61;
        if ( (unsigned __int8)sub_140F54850(a1: a1[132], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F54970(a1: a1[133], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F54A90(a1: a1[134], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        if ( (unsigned __int8)sub_140F54BB0(a1: a1[127], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        sub_140F4BA60(a1: a1[127], a2: a1);
        if ( (unsigned __int8)sub_140F55120(a1: a1[137], a2: &v64, a3: a1) == 0
          || (unsigned __int8)sub_140F55240(a1: a1[138], a2: &v64, a3: a1) == 0
          || *((unsigned __int16 *)a1 + 708) >= 0xDECu
          && (unsigned __int8)sub_140F55360(a1: a1[139], a2: &v64, a3: a1) == 0 )
        {
          goto LABEL_150;
        }
        if ( (unsigned __int8)sub_140F55480(a1: a1[136], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        sub_140F4BBD0(a1: a1[136], a2: a1);
        if ( (unsigned __int8)sub_140F555A0(a1: a1[140], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        sub_140F4BC60(a1: a1[140], a2: a1);
      }
      if ( (unsigned __int8)sub_1400015E0(a1: v53, a2: v52, a3: v54, a4: v55, a5: v63) != 0 )
      {
        if ( (unsigned __int8)sub_140F556C0(a1: a1[118], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        sub_140F4B810(a1: a1[118], a2: a1);
        if ( (unsigned __int8)sub_140F557E0(a1: a1[119], a2: &v64, a3: a1) == 0 )
          goto LABEL_150;
        sub_140F4B910(a1: a1[119], a2: a1);
      }
LABEL_145:
      if ( (unsigned __int8)sub_140F55900(a1: a1[2], a2: &v64, a3) == 0
        || (unsigned __int8)sub_140F55B20(a1: a1[12], a2: &v64, a3) == 0
        || (_BYTE)a3 != 0 && (unsigned __int8)sub_140F55D40(a1: a1[19], a2: &v64) == 0 )
      {
        goto LABEL_150;
      }
      *((_BYTE *)a1 + 1450) = 0;
      sub_140F55F60(a1);
      *((_WORD *)a1 + 708) = 3569;
      v66 = 0;
      v67 = *(_QWORD *)(*(_QWORD *)(qword_141ABD468 + 8) + 64LL);
      sub_140F50EC0((_DWORD)a1, a2: (unsigned int)&v67, a3: (unsigned int)&v66, a4: 0, a5: 0, a6: 1, a7: 1, a8: 18);
      sub_140F3E690(a1, a2: 0);
      sub_140F56140(a1);
      sub_140F56290(a1);
      LOBYTE(v21) = 1;
LABEL_151:
      v62 = (void (__fastcall ***)(_QWORD, __int64))v64;
      if ( v64 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v64 + 8)) == 0 )
        (**v62)(a1: v62, a2: 1);
LABEL_34:
      v22 = (void (__fastcall ***)(_QWORD, __int64))v70;
      if ( v70 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v70 + 8)) == 0 )
        (**v22)(a1: v22, a2: 1);
      v23 = v69;
      if ( v69 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v69 - 4)) == 0 )
        sub_1412EC9A0(a1: v23 - 4);
      return (unsigned int)v21;
    }
  }
  LODWORD(v21) = 0;
  goto LABEL_34;
}
