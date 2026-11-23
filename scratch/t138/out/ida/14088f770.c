__int64 __fastcall sub_14088F770(__int64 a1, __int64 *a2, char a3, __int64 a4, __int64 a5, char a6, char a7)
{
  __int64 v7; // r15
  char v8; // bl
  char v11; // r14
  volatile signed __int32 **v12; // rdi
  __int64 *v15; // rax
  __int64 *v16; // rdx
  __int64 *v17; // rcx
  __int64 *v18; // rbx
  volatile signed __int32 *v19; // rcx
  volatile signed __int32 *v20; // rsi
  __int64 v21; // rax
  __int64 v22; // rdx
  __int64 v23; // rcx
  __int64 v24; // rbx
  bool v25; // al
  volatile signed __int32 *v26; // rax
  volatile signed __int32 *v27; // rcx
  volatile signed __int32 *v28; // rax
  volatile signed __int32 *v29; // rcx
  volatile signed __int32 *v30; // rcx
  void (__fastcall ***v31)(_QWORD, __int64); // rcx
  __int64 v32; // rdx
  __int64 v33; // rax
  __int64 result; // rax
  __int64 v35; // rcx
  volatile signed __int32 *v36; // rsi
  volatile signed __int32 *v37; // rsi
  volatile signed __int32 *v38; // rsi
  __int64 v39; // rax
  __int64 v40; // rax
  __int64 v41; // rcx
  int v42; // esi
  __int64 v43; // rax
  int v44; // r8d
  __int64 v45; // rsi
  __int64 v46; // r8
  volatile signed __int32 *v47; // rcx
  volatile signed __int32 *v48; // rcx
  __int64 v49; // [rsp+48h] [rbp-38h] BYREF
  volatile signed __int32 *v50; // [rsp+50h] [rbp-30h] BYREF
  volatile signed __int32 *v51[3]; // [rsp+58h] [rbp-28h] BYREF
  __int16 v52; // [rsp+76h] [rbp-Ah] BYREF
  _QWORD v53[2]; // [rsp+78h] [rbp-8h] BYREF
  volatile signed __int32 *v54; // [rsp+88h] [rbp+8h] BYREF
  __int64 v55; // [rsp+90h] [rbp+10h] BYREF
  char v56; // [rsp+9Eh] [rbp+1Eh] BYREF
  char v57; // [rsp+9Fh] [rbp+1Fh] BYREF
  __int64 v58; // [rsp+A0h] [rbp+20h]

  v58 = -2;
  v7 = a4;
  v8 = a3;
  v11 = a6;
  v12 = (volatile signed __int32 **)(a1 + 208);
  if ( *(_QWORD *)(a1 + 208) == 0 )
  {
    v51[0] = nullptr;
    v15 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    v16 = (__int64 *)v15[1];
    v17 = v15;
    if ( *((_BYTE *)v16 + 25) == 0 )
    {
      v17 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
      do
      {
        v18 = v16 + 2;
        if ( v16[4] >= (unsigned __int64)qword_141B5ACC0 )
        {
          v17 = v16;
          v18 = v16;
        }
        v16 = (__int64 *)*v18;
      }
      while ( *(_BYTE *)(*v18 + 25) == 0 );
    }
    if ( *((_BYTE *)v17 + 25) != 0 || qword_141B5ACC0 < (unsigned __int64)v17[4] || v17 == v15 )
    {
      v54 = nullptr;
    }
    else
    {
      v26 = (volatile signed __int32 *)v17[5];
      v54 = v26;
      if ( v26 != nullptr )
        _InterlockedIncrement(v26 + 2);
    }
    sub_1407C3450(a1: v53, a2: &v54, a3: v51);
    v19 = v54;
    if ( v54 != nullptr && _InterlockedDecrement(v54 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v19)(a1: v19, a2: 1);
    v20 = v51[0];
    v21 = a4;
    if ( v51[0] != nullptr && _InterlockedDecrement(v51[0]) == 0 )
    {
      sub_1408B5D70(a1: *(_QWORD *)(*((_QWORD *)v20 + 1) + 8LL));
      v22 = *((_QWORD *)v20 + 1);
      if ( v22 != 0 )
      {
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v23 = *(_QWORD *)(qword_141ABD470 + 24),
              (unsigned __int64)(*(_QWORD *)(qword_141ABD470 + 32) - v23) >= 0x181)
          && (v24 = *(_QWORD *)(v23 + 384)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v24 + 32, a2: v22 - *(unsigned int *)(v24 + 120));
          v25 = *(_BYTE *)(v24 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 64)) != 0;
          if ( !v25 && *(_BYTE *)(v24 + 97) != 0 )
            sub_1412D33C0(a1: v24);
        }
        else
        {
          MEMORY[0x141948990](a1: v22 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      sub_141750CFC(a1: v20);
      v21 = a4;
    }
    v11 = a6;
    v8 = a3;
    v7 = v21;
    if ( v53[0] != 0 )
    {
      sub_14080D0E0(a1: &v49, a2: 0x14191EB1BLL);
      v51[0] = (volatile signed __int32 *)0x80100004E554C4CLL;
      sub_1407D0F70(
        a1: (unsigned int)v51,
        a2: (unsigned int)&v54,
        a3: (unsigned int)v53,
        a4: (unsigned int)&qword_141B5ACC8,
        a5: (__int64)&v49,
        a6: 4,
        a7: 0,
        a8: 0);
      v27 = *(volatile signed __int32 **)(a1 + 200);
      if ( v27 == v54 )
      {
        if ( v27 != nullptr && _InterlockedDecrement(v27 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v27)(a1: v27, a2: 1);
        v28 = *(volatile signed __int32 **)(a1 + 200);
        if ( v28 == nullptr )
          goto LABEL_45;
      }
      else
      {
        if ( v27 != nullptr && _InterlockedDecrement(v27 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v27)(a1: v27, a2: 1);
        v28 = v54;
        *(_QWORD *)(a1 + 200) = v54;
        if ( v28 == nullptr )
          goto LABEL_45;
      }
      v54 = v28;
      _InterlockedIncrement(v28 + 2);
      sub_1407C5A20(a1: v51, a2: &v54, a3: v53, a4: &qword_141B5ACC8);
      v29 = *v12;
      if ( *v12 == v51[0] )
      {
        if ( v29 != nullptr && _InterlockedDecrement(v29 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v29)(a1: v29, a2: 1);
      }
      else
      {
        if ( v29 != nullptr && _InterlockedDecrement(v29 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v29)(a1: v29, a2: 1);
        *v12 = v51[0];
        v51[0] = nullptr;
      }
      v30 = v54;
      if ( v54 != nullptr && _InterlockedDecrement(v54 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v30)(a1: v30, a2: 1);
LABEL_45:
      v31 = (void (__fastcall ***)(_QWORD, __int64))v53[0];
      if ( v53[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v53[0] + 8LL)) == 0 )
        (**v31)(a1: v31, a2: 1);
    }
  }
  v49 = 0x80100004E554C4CLL;
  v32 = 0x14191EB1BLL;
  if ( v11 != 0 )
    v32 = 0x1418EEAE0LL;
  sub_14080D0E0(a1: v51, a2: v32);
  v53[0] = 0;
  if ( v53 != a2 )
  {
    v33 = *a2;
    if ( *a2 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v33 - 4));
    v53[0] = v33;
  }
  result = sub_1407D0F70(
             a1: (unsigned int)&v49,
             a2: (unsigned int)&v50,
             a3: (_DWORD)v12,
             a4: (unsigned int)v53,
             a5: (__int64)v51,
             a6: 0,
             a7: 0,
             a8: 0);
  v35 = v53[0];
  if ( v53[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v53[0] - 4LL)) == 0 )
    result = sub_1412EC9A0(a1: v35 - 4);
  v36 = v50;
  if ( v50 != nullptr )
  {
    result = (*(__int64 (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v50 + 40LL))(
               a1: v50,
               a2: &v57,
               a3: 1);
    if ( *((_DWORD *)v36 + 4) != 0
      || v57 == 9
      || (v37 = v50,
          result = (*(__int64 (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)v50 + 40LL))(
                     a1: v50,
                     a2: &v52,
                     a3: 2),
          *((_DWORD *)v37 + 4) != 0)
      || (v56 = 0, WORD2(v49) >= 4u)
      && (v38 = v50,
          result = (*(__int64 (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v50 + 40LL))(
                     a1: v50,
                     a2: &v56,
                     a3: 1),
          *((_DWORD *)v38 + 4) != 0) )
    {
LABEL_89:
      v48 = v50;
      if ( v50 != nullptr && _InterlockedDecrement(v50 + 2) == 0 )
        return (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v48)(a1: v48, a2: 1);
      return result;
    }
    v39 = sub_14083D4F0();
    v53[1] = 0;
    v53[0] = v39 + 8;
    sub_1408386A0(a1: v50, a2: v51, a3: v53);
    if ( LODWORD(v51[0]) != 0 )
    {
LABEL_88:
      result = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v53[0] + 16LL))(a1: v53[0], a2: v53);
      goto LABEL_89;
    }
    sub_1407C9510(a1: v51);
    if ( v8 != 0 )
    {
      v40 = sub_14083D4F0();
      v55 = 0;
      if ( &v55 != a2 )
      {
        v41 = *a2;
        if ( *a2 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v41 - 4));
        v55 = v41;
      }
      v54 = (volatile signed __int32 *)(v40 + 136);
      sub_140835380(a1: v51, a2: 1718512748, a3: &v54);
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v54 + 16LL))(
        a1: v54,
        a2: &v54);
      v42 = v52;
      v43 = sub_14083D4F0();
      LODWORD(v55) = v42;
      v54 = (volatile signed __int32 *)(v43 + 40);
      sub_140835380(a1: v51, a2: 1986359923, a3: &v54);
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v54 + 16LL))(
        a1: v54,
        a2: &v54);
      switch ( v57 )
      {
        case 1:
        case 3:
          sub_1408351C0(a1: v51, a2: 1668246896, a3: v53);
          break;
        case 2:
          sub_1408351C0(a1: v51, a2: 1668116595, a3: v53);
          break;
        case 4:
        case 10:
        case 11:
        case 12:
        case 13:
          sub_1408351C0(a1: v51, a2: 1851880553, a3: v53);
          break;
        case 5:
          sub_1408351C0(a1: v51, a2: 1668183145, a3: v53);
          break;
        default:
          v45 = qword_141B5AD60;
          v54 = nullptr;
          sub_140809040(a1: &v54, a2: 0x14190E225LL, a3: 0xFFFFFFFFLL);
          LOBYTE(v46) = 1;
          (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64, _QWORD))(*(_QWORD *)v45 + 120LL))(
            a1: v45,
            a2: &v54,
            a3: v46,
            a4: 0);
          v47 = v54;
          if ( v54 != nullptr && _InterlockedDecrement(v54 - 1) == 0 )
            sub_1412EC9A0(a1: v47 - 1);
          break;
      }
    }
    else
    {
      sub_140839290(a1: v50, a2: &v54, a3: v51);
      if ( (_DWORD)v54 != 0 )
      {
LABEL_87:
        sub_140833970(a1: v51);
        goto LABEL_88;
      }
    }
    sub_140891560(
      a1,
      a2: (unsigned int)v51,
      a3: v44,
      a4: 0,
      a5: v7,
      a6: a5,
      a7: (__int64)&qword_141B5A458,
      a8: v11,
      a9: a7);
    goto LABEL_87;
  }
  return result;
}
