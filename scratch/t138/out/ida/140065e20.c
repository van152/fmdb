__int64 __fastcall sub_140065E20(__int64 a1, int a2, __int64 a3)
{
  __int64 v3; // rdi
  __int64 v4; // rbx
  __int64 v6; // rdi
  __int64 v7; // rdi
  __int64 v8; // rbx
  unsigned int v9; // eax
  unsigned int v10; // eax
  __int64 v11; // rbx
  char v12; // al
  __int64 v13; // rdi
  __int64 v14; // rdi
  __int64 v16; // rax
  __int64 v17; // rax
  __int64 v18; // rsi
  __int64 v19; // rsi
  void (__fastcall ***v20)(_QWORD, __int64); // rcx
  __int64 v21; // rax
  unsigned int v22; // ebp
  unsigned int v23; // eax
  __int64 v24; // rdi
  unsigned int v25; // eax
  __int64 v26; // rdx
  __int64 v27; // r9
  __int64 v28; // rdi
  _BYTE v29[8]; // [rsp+20h] [rbp-78h] BYREF
  _BYTE v30[16]; // [rsp+28h] [rbp-70h] BYREF
  _QWORD v31[12]; // [rsp+38h] [rbp-60h] BYREF

  v3 = a3;
  LODWORD(v4) = a2;
  if ( a2 <= 1935894120 )
  {
    if ( a2 > 1668052082 )
    {
      if ( a2 > 1836413032 )
      {
        if ( a2 > 1919316578 )
        {
          if ( a2 == 1919316579 )
          {
            sub_140064C30(a1);
            goto LABEL_89;
          }
          if ( a2 == 1919705971 )
          {
            sub_140064C30(a1);
            sub_140067B80(a1);
            sub_140067DD0(a1);
          }
        }
        else
        {
          if ( a2 == 1836413033 )
            return sub_1400685A0(a1, a2: a3);
          if ( a2 == 1852992609 )
          {
            sub_140064C30(a1);
            sub_140067670(a1);
            sub_140067940(a1);
            sub_140067220(a1);
            sub_140146740(a1: v31, a2: 1313820229, a3: 0);
            v8 = qword_141ABF5C0;
            v9 = sub_1401270C0(a1);
            v10 = sub_140012880(a1: v8, a2: v9);
            sub_14083D790(a1: v30, a2: v10);
            sub_140835380(a1: v31, a2: 1701079412, a3: v30);
            sub_14083D320(a1: v30);
            v11 = qword_141ABF5C0;
            v12 = sub_1401270C0(a1);
            sub_140835E50(a1: v31, a2: v11 + 264LL * v12 + 44792);
            v4 = qword_141ABF5C0;
            *(_BYTE *)(v4 + 264LL * (char)sub_1401270C0(a1) + 44784) = -1;
            sub_1400669F0(a1, a2: v31);
            sub_140833970(a1: v31);
            goto LABEL_89;
          }
        }
        return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
      }
      if ( a2 <= 1701078129 )
      {
        if ( a2 == 1668052083 )
        {
          sub_140048080(a1: v31);
          v18 = v31[0];
          if ( v31[0] != 0 )
          {
            sub_1407D8AB0(a1: v30, a2: 0x1418E2C24LL);
            sub_1407D19F0(a1: v18, a2: v29, a3: v30, a4: 3);
          }
          v19 = qword_141ABD830;
          sub_140051C40(a1: qword_141ABD830 + 1432);
          *(_BYTE *)(v19 + 1424) = 0;
          *(_BYTE *)(v19 + 1512) = 0;
          v20 = (void (__fastcall ***)(_QWORD, __int64))v31[0];
          if ( v31[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31[0] + 8LL)) == 0 )
            (**v20)(a1: v20, a2: 1);
          goto LABEL_89;
        }
        if ( a2 == 1684825205 )
        {
          sub_1400393E0(a1: *(_QWORD *)(a1 + 504));
          goto LABEL_89;
        }
        return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
      }
      if ( a2 == 1701078130 )
      {
        sub_1400684A0(a1, a2: a3);
        goto LABEL_89;
      }
      if ( a2 != 1818522995 )
        return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
      sub_140039040(a1: *(_QWORD *)(a1 + 504));
      goto LABEL_78;
    }
    if ( a2 > 1431192654 )
    {
      if ( a2 > 1667527282 )
      {
        if ( a2 == 1667527283 )
        {
          sub_140066C80(a1, a2: a3);
          goto LABEL_89;
        }
        if ( a2 == 1667789417 )
          return sub_1400669F0(a1, a2: a3);
      }
      else
      {
        if ( a2 == 1431192655 )
        {
          v21 = sub_140835850(a1: a3, a2: 1768169504);
          v22 = sub_14083E0C0(a1: v21);
          v4 = qword_141ABF5C0;
          v23 = sub_1401270C0(a1);
          sub_14001CC80(a1: v4, a2: v23, a3: v22, a4: a1 + 408);
          goto LABEL_89;
        }
        if ( a2 == 1651209078 )
        {
          *(_BYTE *)(qword_141ABD830 + 1358) ^= 1u;
          goto LABEL_89;
        }
      }
      return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
    }
    if ( a2 == 1145455686 )
    {
      sub_140066840(a1, a2: a3);
      goto LABEL_89;
    }
    if ( a2 != 1181632108 )
    {
      if ( a2 == 1396786246 )
      {
        sub_140066780(a1, a2: a3);
        goto LABEL_89;
      }
      return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
    }
    v24 = qword_141ABF5C0;
    v25 = sub_1401270C0(a1);
    sub_1400244F0(a1: v24, a2: v25, a3: v31);
    if ( LODWORD(v31[0]) == 25 )
    {
      v27 = 1668115571;
    }
    else
    {
      if ( LODWORD(v31[0]) != 9 )
      {
LABEL_88:
        sub_140127370(a1);
        goto LABEL_89;
      }
      v27 = 1853123699;
    }
    LOBYTE(v26) = 1;
    sub_140064B40(a1, a2: v26, a3: 0xFFFFFFFFLL, a4: v27);
    goto LABEL_88;
  }
  if ( a2 > 1937337970 )
  {
    if ( a2 > 1970303605 )
    {
      if ( a2 > 1970499948 )
      {
        if ( a2 == 1970499949 )
        {
          *(_BYTE *)(qword_141ABD830 + 1371) ^= 1u;
          goto LABEL_89;
        }
        if ( a2 == 1970501487 )
        {
          *(_BYTE *)(qword_141ABD830 + 1349) ^= 1u;
          goto LABEL_89;
        }
        return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
      }
      if ( a2 != 1970303606 )
      {
        if ( a2 != 1970499681 )
          return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
LABEL_43:
        LOBYTE(v4) = 1;
        LOBYTE(a3) = 1;
        sub_1400670B0(a1, a2: 0, a3);
        return (unsigned int)v4;
      }
    }
    else
    {
      if ( a2 <= 1952936824 )
      {
        if ( a2 == 1937337971 )
        {
          sub_140066E80(a1, a2: a3);
          goto LABEL_89;
        }
        if ( a2 != 1952737638 )
          return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
        v6 = qword_141ABF5C0;
        LODWORD(v4) = *(unsigned __int8 *)(v6 + 264LL * (char)sub_1401270C0(a1) + 45014);
        *(_BYTE *)(v6 + 264LL * (char)sub_1401270C0(a1) + 45014) = v4 ^ 1;
        v7 = qword_141ABF5C0;
        *(_BYTE *)(v7 + 264LL * (char)sub_1401270C0(a1) + 45015) = 0;
        goto LABEL_43;
      }
      if ( a2 != 1952936825 )
      {
        if ( a2 == 1970303593 )
        {
          sub_140067670(a1);
          goto LABEL_89;
        }
        return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
      }
      v28 = qword_141ABF5C0;
      LODWORD(v4) = *(unsigned __int8 *)(v28 + 264LL * (char)sub_1401270C0(a1) + 45013);
      *(_BYTE *)(v28 + 264LL * (char)sub_1401270C0(a1) + 45013) = v4 ^ 1;
    }
    sub_140067220(a1);
    goto LABEL_89;
  }
  if ( a2 <= 1936483185 )
  {
    if ( a2 <= 1935958645 )
    {
      if ( a2 == 1935894121 )
      {
        sub_140065C80(a1, a2: a3);
        goto LABEL_89;
      }
      if ( a2 == 1935895929 )
      {
        *(_BYTE *)(qword_141ABD830 + 1350) ^= 1u;
LABEL_89:
        LOBYTE(v4) = 1;
        return (unsigned int)v4;
      }
      return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
    }
    if ( a2 != 1935958646 )
    {
      if ( a2 != 1935960422 )
        return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
      v13 = qword_141ABF5C0;
      LODWORD(v4) = *(unsigned __int8 *)(v13 + 264LL * (char)sub_1401270C0(a1) + 45015);
      *(_BYTE *)(v13 + 264LL * (char)sub_1401270C0(a1) + 45015) = v4 ^ 1;
      v14 = qword_141ABF5C0;
      *(_BYTE *)(v14 + 264LL * (char)sub_1401270C0(a1) + 45014) = 0;
      goto LABEL_43;
    }
    sub_140125F80(a1);
    sub_140127370(a1);
LABEL_78:
    sub_140147750(a1, a2: 1919705960, a3: 0);
    goto LABEL_89;
  }
  if ( a2 <= 1936738627 )
  {
    if ( a2 == 1936483186 )
      return sub_140066D40(a1, a2: a3);
    if ( a2 == 1936483426 )
    {
      sub_1400665D0(a1, a2: a3);
      goto LABEL_89;
    }
    return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
  }
  if ( a2 == 1936738628 )
  {
    *(_BYTE *)(qword_141ABD830 + 1351) ^= 1u;
    goto LABEL_89;
  }
  if ( a2 != 1937142371 )
    return sub_140124EF0(a1, a2: (unsigned int)v4, a3: v3);
  sub_140146740(a1: v31, a2: 1818518374, a3: 0);
  v16 = sub_140835850(a1: v3, a2: 1952807028);
  sub_1408351C0(a1: v31, a2: 1936091500, a3: v16);
  sub_1407D8AB0(a1: v29, a2: 0x1418E2C24LL);
  v17 = sub_140179440(a1: v29);
  sub_14083D970(a1: v30, a2: v17);
  sub_140835380(a1: v31, a2: 1937013104, a3: v30);
  sub_14083D320(a1: v30);
  LODWORD(v4) = sub_140147670(a1, a2: v31);
  sub_140833970(a1: v31);
  return (unsigned int)v4;
}
