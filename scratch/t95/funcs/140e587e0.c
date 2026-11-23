__int64 __fastcall sub_140E587E0(__int64 a1, __int64 a2, __int64 a3, _QWORD *a4)
{
  unsigned int v4; // ebp
  __int64 v7; // rbx
  unsigned int v8; // eax
  int v9; // ecx
  __int64 v11; // rcx
  __int64 v12; // rsi
  char v13; // al
  char v14; // cl
  char v15; // al
  int v16; // ecx
  unsigned int v17; // eax
  volatile signed __int32 *v18; // rcx
  __int64 v19; // rcx
  __int64 v20; // rsi
  char v21; // al
  char v22; // cl
  char v23; // al
  volatile signed __int32 **v24; // [rsp+28h] [rbp-60h] BYREF
  _QWORD *v25; // [rsp+30h] [rbp-58h] BYREF
  volatile signed __int32 *v26; // [rsp+38h] [rbp-50h] BYREF
  _QWORD v27[4]; // [rsp+40h] [rbp-48h] BYREF
  char v28; // [rsp+60h] [rbp-28h]

  if ( a1 == 0 )
  {
    sub_140F4AEF0((__int64)&qword_141B5FDA8, a3, a4);
    LOBYTE(v4) = 1;
    return v4;
  }
  v7 = a1;
  LOBYTE(v4) = 1;
  if ( (int)a3 <= 1130652275 )
  {
    if ( (int)a3 > 1130588768 )
    {
      if ( (unsigned int)(a3 - 1130588769) > 0x18 || (v9 = 17600973, !_bittest(&v9, a3 - 1130588769)) )
      {
        if ( (unsigned int)(a3 - 1130591074) > 0x17 )
          goto LABEL_120;
        v16 = 8471121;
        if ( _bittest(&v16, a3 - 1130591074) )
          return sub_14151ED80(v7 + 224, (unsigned int)a3, a4);
        if ( (_DWORD)a3 != 1130591091 )
        {
LABEL_120:
          if ( (_DWORD)a3 != 1130590307 )
            return 0;
        }
      }
      return sub_141520380(v7 + 231, (unsigned int)a3, a4);
    }
    if ( (int)a3 <= 1130443629 )
    {
      if ( (int)a3 <= 1129263981 )
      {
        if ( (_DWORD)a3 == 1128361314 )
        {
          v26 = (volatile signed __int32 *)a2;
          sub_141449D60(v27, a2);
          v24 = &v26;
          v25 = v27;
          v8 = sub_140DF7BC0(&v24, a4);
          goto LABEL_115;
        }
        if ( (_DWORD)a3 == 1128481379 )
        {
          v26 = (volatile signed __int32 *)a2;
          LOBYTE(a3) = 4;
          sub_141522B80(v27, a2, a3);
          v28 = 4;
LABEL_114:
          v24 = &v26;
          v25 = v27;
          v8 = sub_140EA1030(&v24, a4);
LABEL_115:
          v4 = v8;
          if ( v27[0] != 0 )
            sub_1407E4890(qword_141ABD470, v27[0], v27[2] - v27[0]);
          return v4;
        }
        return 0;
      }
      if ( (_DWORD)a3 != 1129263982 )
      {
        if ( (_DWORD)a3 != 1129538384 )
          return 0;
        *(_BYTE *)(a1 + 295) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
      }
    }
    else
    {
      if ( (int)a3 > 1130521195 )
      {
        if ( (_DWORD)a3 != 1130521196 )
        {
          if ( (_DWORD)a3 != 1130587233 && (_DWORD)a3 != 1130587250 )
            return 0;
          return sub_141520380(v7 + 231, (unsigned int)a3, a4);
        }
        v26 = (volatile signed __int32 *)a2;
        LOBYTE(a3) = 7;
        sub_141522B80(v27, a2, a3);
        v28 = 7;
        goto LABEL_114;
      }
      if ( (_DWORD)a3 != 1130443630 )
      {
        if ( (_DWORD)a3 == 1130458467 )
        {
          v26 = (volatile signed __int32 *)a2;
          LOBYTE(a3) = 6;
          sub_141522B80(v27, a2, a3);
          v28 = 6;
          goto LABEL_114;
        }
        return 0;
      }
      if ( (*(_BYTE *)(a2 + 352) & 4) == 0 )
      {
        (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, _QWORD *))(*(_QWORD *)*a4 + 128LL))(*a4, &v26, a4);
        v7 += 16;
LABEL_97:
        sub_140809100(v7, &v26);
        v18 = v26;
        if ( v26 != nullptr && _InterlockedDecrement(v26 - 1) == 0 )
          sub_1412EC9A0((__int64)(v18 - 1));
        return v4;
      }
    }
    return v4;
  }
  if ( (int)a3 > 1131638884 )
  {
    if ( (int)a3 > 1131897707 )
    {
      if ( (int)a3 <= 1132030316 )
      {
        if ( (_DWORD)a3 == 1131897708 )
        {
          v26 = (volatile signed __int32 *)a2;
          sub_141524900(v27, a2);
          v24 = &v26;
          v25 = v27;
          v8 = sub_140EA2880(&v24, a4);
          goto LABEL_115;
        }
        if ( (_DWORD)a3 != 1132029538 )
        {
          if ( (_DWORD)a3 == 1132029550 )
          {
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 8LL))(*a4, a4) != 0 )
              *(_WORD *)(v7 + 216) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 80LL))(*a4, a4);
            else
              *(_WORD *)(v7 + 216) = 0;
            return v4;
          }
          return 0;
        }
        *(_BYTE *)(a1 + 299) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
      }
      else if ( (int)a3 > 1413705576 )
      {
        if ( (_DWORD)a3 == 1885565044 )
        {
          v24 = (volatile signed __int32 **)a2;
          v25 = (_QWORD *)a2;
          v26 = (volatile signed __int32 *)&v24;
          v27[0] = &v25;
          return (unsigned int)sub_140EA3420(&v26, a4);
        }
        else
        {
          if ( (_DWORD)a3 != 1413705577 )
            return 0;
          *(_DWORD *)(a1 + 204) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
        }
      }
      else
      {
        if ( (_DWORD)a3 != 1132030317 )
        {
          if ( (_DWORD)a3 == 1132033142 )
          {
            *(_BYTE *)(a1 + 300) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
            if ( (unsigned __int8)sub_140087040() != 0 )
            {
              v11 = *(_QWORD *)(a2 + 336);
              if ( v11 != 0 && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v11 + 56LL))(v11) == 1 )
              {
                v12 = *(_QWORD *)(a2 + 336);
                if ( v12 != 0 )
                {
                  v13 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
                  v14 = 20;
                  if ( v13 < 20 )
                    v14 = v13;
                  v15 = 1;
                  if ( v14 >= 2 )
                    v15 = v14;
                  *(_BYTE *)(v12 + 2226) = v15;
                }
              }
            }
            return v4;
          }
          return 0;
        }
        *(_BYTE *)(a1 + 294) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
      }
      return v4;
    }
    if ( (int)a3 > 1131639911 )
    {
      switch ( (_DWORD)a3 )
      {
        case 0x43737468:
          *(_DWORD *)(a1 + 192) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
          break;
        case 0x4373786E:
          if ( (*(_BYTE *)(a2 + 352) & 4) == 0 )
          {
            (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, _QWORD *))(*(_QWORD *)*a4 + 128LL))(
              *a4,
              &v26,
              a4);
            goto LABEL_97;
          }
          break;
        case 0x43746C76:
          *(_BYTE *)(a1 + 288) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
          break;
        default:
          return 0;
      }
      return v4;
    }
    if ( (unsigned int)(a3 - 1131638899) >= 2 && (_DWORD)a3 != 1131638885 && (_DWORD)a3 != 1131639909 )
      return 0;
    return sub_1415219F0(a1 + 248, (unsigned int)a3, a4);
  }
  if ( (int)a3 > 1131374957 )
  {
    if ( (int)a3 <= 1131635045 )
    {
      switch ( (_DWORD)a3 )
      {
        case 0x436F696E:
          v24 = (volatile signed __int32 **)a2;
          v25 = (_QWORD *)a2;
          v26 = (volatile signed __int32 *)&v24;
          v27[0] = &v25;
          return (unsigned int)sub_140E9D190(&v26, a4);
        case 0x43726362:
          *(_BYTE *)(a1 + 301) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
          if ( (unsigned __int8)sub_140087040() != 0 )
          {
            v19 = *(_QWORD *)(a2 + 336);
            if ( v19 != 0 && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v19 + 56LL))(v19) == 1 )
            {
              v20 = *(_QWORD *)(a2 + 336);
              if ( v20 != 0 )
              {
                v21 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
                v22 = 20;
                if ( v21 < 20 )
                  v22 = v21;
                v23 = 1;
                if ( v22 >= 2 )
                  v23 = v22;
                *(_BYTE *)(v20 + 2227) = v23;
              }
            }
          }
          return v4;
        case 0x43726B74:
          v17 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
          sub_140E590A0(a2, v17);
          break;
        default:
          return 0;
      }
      return v4;
    }
    if ( (int)a3 > 1131638626 )
    {
      if ( (_DWORD)a3 == 1131638627 )
      {
        v26 = (volatile signed __int32 *)a2;
        LOBYTE(a3) = 5;
        sub_141522B80(v27, a2, a3);
        v28 = 5;
        goto LABEL_114;
      }
      if ( (_DWORD)a3 != 1131638882 )
        return 0;
      v24 = (volatile signed __int32 **)a2;
      v25 = (_QWORD *)a2;
      v26 = (volatile signed __int32 *)&v24;
      v27[0] = &v25;
      return (unsigned int)sub_140E9C680(&v26, a4);
    }
    if ( (_DWORD)a3 != 1131635046 && (_DWORD)a3 != 1131637881 )
      return 0;
    return sub_1415219F0(a1 + 248, (unsigned int)a3, a4);
  }
  if ( (int)a3 <= 1131164525 )
  {
    switch ( (_DWORD)a3 )
    {
      case 0x43646274:
        v26 = (volatile signed __int32 *)a2;
        a3 = 0;
        break;
      case 0x43666670:
        v26 = (volatile signed __int32 *)a2;
        LOBYTE(a3) = 1;
        break;
      case 0x43666C6E:
        v24 = (volatile signed __int32 **)a2;
        v25 = (_QWORD *)a2;
        v26 = (volatile signed __int32 *)&v24;
        v27[0] = &v25;
        return (unsigned int)sub_140E9F690(&v26, a4);
      default:
        return 0;
    }
    sub_141522140(v27, a2, a3);
    v24 = &v26;
    v25 = v27;
    v8 = sub_140E9E8E0(&v24, a4);
    goto LABEL_115;
  }
  if ( (int)a3 > 1131244644 )
  {
    if ( (_DWORD)a3 != 1131244645 )
    {
      if ( (_DWORD)a3 == 1131246697 )
      {
        v26 = (volatile signed __int32 *)a2;
        sub_141524510(v27, a2);
        v24 = &v26;
        v25 = v27;
        v8 = sub_140EA1CD0(&v24, a4);
        goto LABEL_115;
      }
      return 0;
    }
    *(_BYTE *)(a1 + 289) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 64LL))(*a4, a4);
  }
  else
  {
    if ( (_DWORD)a3 != 1131164526 )
    {
      if ( (_DWORD)a3 == 1131178099 )
      {
        v26 = (volatile signed __int32 *)a2;
        sub_141522730(v27, a2);
        v24 = &v26;
        v25 = v27;
        v8 = sub_140EA0500(&v24, a4);
        goto LABEL_115;
      }
      return 0;
    }
    if ( (*(_BYTE *)(a2 + 352) & 4) == 0 )
    {
      (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, _QWORD *))(*(_QWORD *)*a4 + 128LL))(*a4, &v26, a4);
      v7 += 8;
      goto LABEL_97;
    }
  }
  return v4;
}
